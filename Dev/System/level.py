import pygame 

from aniblock import AnimationBlock
from data import MapData, SaveData, SettingData
from debug import debug
from event.eventctrl import EventCtrl
from key import KeyPress, KeySettings
from menu import Menu
from player import Player
from savepage import SavePage
from settings import *
from sound import BGM, BGS, SE, choose_sound
from support import import_csv_layout, import_folder
from tile import Tile

class Level:
    def __init__(self, eventctrl: EventCtrl, 
                 map_data: MapData, save_data: SaveData, setting_data: SettingData, 
                 menu: Menu, savepage: SavePage) -> None:
        self.eventctrl = eventctrl

        # map data
        self.map_data = map_data
        self.csv_map_path = self.map_data["csvMap"]
        self.ground_filename = self.map_data["ground"]

        self.save_data = save_data
        self.setting_data = setting_data

        # init sound volume
        BGM.set_global_volume(self.setting_data["volume"]["BGM"])
        BGS.set_global_volume(self.setting_data["volume"]["BGS"])
        SE.set_global_volume(self.setting_data["volume"]["SE"])

        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup(self.ground_filename)
        self.obstacle_sprites = pygame.sprite.Group()
        self.event_sprites = pygame.sprite.Group()
        self.groundtype_sprites = pygame.sprite.Group()

        # menu
        self.menu = menu
        self.is_menu_listening = False
        self.is_menu_open = False
        self.forced_menu_listening = False

        # sprite setup (including player)
        self.create_map()

        # save
        self.savepage = savepage
        self.is_saving = False

        # sound settings
        # background music/sound
        self.bgm = None
        self.bgs = None
        self.play_bgm_and_bgs()
        # sound effects
        # walking sound
        self.ground_SE_dict = {}
        self.walking_sound_id = None
        self.load_walking_sound()

        # start map
        self.is_start_map_animate = True
        self.start_map_surf = pygame.surface.Surface((WIDTH, HEIGTH)).convert_alpha()
        self.start_map_surf_alpha = 255
        self.start_map_surf.set_alpha(255)

        # dark cover
        self.dark_cover_surf: pygame.Surface | None = None

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout(self.csv_map_path + '/map_FloorBlocks.csv'),
            'object': import_csv_layout(self.csv_map_path + '/map_Objects.csv'),
            'entities': import_csv_layout(self.csv_map_path + '/map_Entities.csv'), 
            'event': import_csv_layout(self.csv_map_path + '/map_Events.csv'), 
            'detail': import_csv_layout(self.csv_map_path + '/map_Details.csv'), 
            'groundtype': import_csv_layout(self.csv_map_path + '/map_Groundtype.csv'), 
            'animationblockobject': import_csv_layout(self.csv_map_path + '/map_AnimationBlockObjects.csv'), 
            'animationblockdetail': import_csv_layout(self.csv_map_path + '/map_AnimationBlockDetails.csv')
        }
        graphics = {
            'objects': import_folder('../Graphics/objects'), 
            'details': import_folder('../Graphics/details')
        }

        # create player
        player_status = self.save_data["player-status"]
        x = player_status["pos"][0] * TILESIZE
        y = player_status["pos"][1] * TILESIZE
        self.player = Player(
            (x,y),
            [self.visible_sprites],
            self.obstacle_sprites, 
            player_status["status"]
        )

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'detail':
                            surf = graphics['details'][int(col)]
                            Tile((x,y), [self.visible_sprites], 'detail', surf)

                        if style == 'event':
                            Tile((x,y), [self.event_sprites], 'event', event_id = int(col))

                        if style == 'groundtype':
                            Tile((x,y), [self.groundtype_sprites], 'groundtype', ground_id = int(col))

                        if style == 'animationblockobject':
                            AnimationBlock((col_index, row_index), 
                                           [self.visible_sprites, self.obstacle_sprites], 
                                           int(col))

                        if style == 'animationblockdetail':
                            AnimationBlock((col_index, row_index), 
                                           [self.visible_sprites], 
                                           int(col))

                        if style == 'entities': # except player
                            pass 

    def load_walking_sound(self):
        for item in self.map_data["ground-SE"]:
            sound = SE(item["path"])
            sound.set_global_volume(self.setting_data["volume"]["SE"])
            self.ground_SE_dict.update({item["id"]: sound})

    def play_bgm_and_bgs(self):
        path = self.map_data["BGM"]
        if path is not None:
            self.bgm = BGM(path)
            self.bgm.set_global_volume(self.setting_data["volume"]["BGM"])
            self.bgm.play(-1)
        path = self.map_data["BGS"]
        if path is not None:
            self.bgs = BGS(path)
            self.bgs.set_global_volume(self.setting_data["volume"]["BGS"])
            self.bgs.play(-1)

    def stop_bgm_and_bgs(self):
        BGM.stop_all()
        BGS.stop_all()

    def play_walking_sound(self):
        if self.player.direction.x == 0 and self.player.direction.y == 0:
            for index, sound in self.ground_SE_dict.items():
                sound.stop()
            self.walking_sound_id = None
            return 
        # walking sound collision
        is_collided = False
        for sprite in self.groundtype_sprites:
            if sprite.hitbox.colliderect(self.player.hitbox):
                ground_id = sprite.ground_id
                if self.walking_sound_id != ground_id:
                    for sound in self.ground_SE_dict.values():
                        sound.stop()
                    self.ground_SE_dict[ground_id].play(-1)
                    self.walking_sound_id = ground_id
                is_collided = True
        if not is_collided:
            for sound in self.ground_SE_dict.values():
                sound.stop()
            self.walking_sound_id = None

    def lock_player(self):
        self.player.is_keyboard_forbidden = True
        self.player.direction.x, self.player.direction.y = 0, 0
    
    def unlock_player(self):
        self.player.is_keyboard_forbidden = False

    def menu_listener(self):
        if self.player.is_keyboard_forbidden and not self.forced_menu_listening:
            return 
        keys = KeyPress.keys
        if keys[KeySettings.menu_1] or keys[KeySettings.menu_2]:
            if self.is_menu_listening:
                self.is_menu_listening = False
                self.lock_player()
                choose_sound.play()
                self.is_menu_open = True
        else:
            self.is_menu_listening = True

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        if self.dark_cover_surf is not None:
            self.display_surface.blit(self.dark_cover_surf, (0,0))

        # start map animate
        if self.is_start_map_animate:
            self.lock_player()
            self.display_surface.blit(self.start_map_surf, (0,0))
            speed = 4
            self.start_map_surf_alpha -= speed
            if self.start_map_surf_alpha < 0:
                self.is_start_map_animate = False
                self.unlock_player()
            else:
                self.start_map_surf.set_alpha(self.start_map_surf_alpha)
            return

        # play walk sound
        self.play_walking_sound()
        
        if self.is_menu_open:
            self.eventctrl.is_event_listening = False # avoid z/return/space problem

            # run menu
            self.menu.run()

        elif self.is_saving:
            self.is_menu_listening = False # avoid esc problem

            # run save
            self.savepage.run()

        else:
            # run events
            self.eventctrl.run()

            # update sprites (including player)
            self.visible_sprites.update()

            # listen to menu
            self.menu_listener()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, ground_filename):

        # general setup 
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load(ground_filename).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):

        # getting the offset 
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.bottom):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
