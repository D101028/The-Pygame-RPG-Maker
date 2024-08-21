import pygame 

from settings import *
from tile import Tile
from player import Player
from backup.event import EventCtrl, ChangeMapParam
from menu import Menu
from savepage import SavePage
from debug import debug
from support import *

class Level:
    def __init__(self, save_data, map_name, change_map_param = None):
        # load data
        self.data = save_data["map-details"][map_name]
        self.csv_map_path = self.data["csvMap"]
        self.ground_filename = self.data["ground"]

        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup(self.ground_filename)
        self.obstacle_sprites = pygame.sprite.Group()
        self.event_sprites = pygame.sprite.Group()
        self.groundtype_sprites = pygame.sprite.Group()

        # menu
        self.menu = Menu(save_data)
        self.is_menu_listening = False
        self.is_menu_open = False

        # sprite setup (including player)
        self.create_map()

        # save
        self.savepage = SavePage(self.menu, self.player)
        self.is_saving = False

        # event class
        self.eventctrl = EventCtrl(self.player, self.event_sprites, map_name, change_map_param, self.menu)

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

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout(self.csv_map_path + '/map_FloorBlocks.csv'),
            'object': import_csv_layout(self.csv_map_path + '/map_Objects.csv'),
            'entities': import_csv_layout(self.csv_map_path + '/map_Entities.csv'), 
            'event': import_csv_layout(self.csv_map_path + '/map_Events.csv'), 
            'detail': import_csv_layout(self.csv_map_path + '/map_Details.csv'), 
            'groundtype': import_csv_layout(self.csv_map_path + '/map_Groundtype.csv')
        }
        graphics = {
            'objects': import_folder('../Graphics/objects'), 
            'details': import_folder('../Graphics/details')
        }

        # create player
        player_status = self.menu.save_data["player-status"]
        x = player_status["pos"][0] * TILESIZE
        y = player_status["pos"][1] * TILESIZE
        self.player = Player(
            (x,y),
            [self.visible_sprites],
            self.obstacle_sprites, 
        )
        self.player.status = player_status["status"]

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
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

                        if style == 'entities':
                            pass 

    def load_walking_sound(self):
        for item in self.data["ground-SE"]:
            sound = pygame.mixer.Sound(item["path"])
            sound.set_volume(self.menu.settings["volume"]["SE"])
            self.ground_SE_dict.update({item["id"]: sound})

    def play_bgm_and_bgs(self):
        path = self.data["BGM"]
        if path is not None:
            self.bgm = pygame.mixer.Sound(path)
            self.bgm.set_volume(self.menu.settings["volume"]["BGM"])
            self.bgm.play(-1)
        path = self.data["BGS"]
        if path is not None:
            self.bgs = pygame.mixer.Sound(path)
            self.bgs.set_volume(self.menu.settings["volume"]["BGS"])
            self.bgs.play(-1)

    def stop_bgm_and_bgs(self):
        if self.bgm is not None:
            self.bgm.stop()
        if self.bgs is not None:
            self.bgs.stop()

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

    def set_sound_value(self):
        for sound in self.ground_SE_dict.values():
            sound.set_volume(self.menu.settings["volume"]["SE"])
        if self.bgm is not None:
            self.bgm.set_volume(self.menu.settings["volume"]["BGM"])
        if self.bgs is not None:
            self.bgs.set_volume(self.menu.settings["volume"]["BGS"])

    def menu_listener(self):
        if len(self.eventctrl.processes) != 0:
            return 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if self.is_menu_listening:
                self.is_menu_listening = False
                self.menu.choose_sound.play()
                self.is_menu_open = True
        else:
            self.is_menu_listening = True

    def run(self):
        """return ChangeMapParam or MenuReturnParam"""
        self.is_saving = self.eventctrl.is_open_saving
        self.visible_sprites.custom_draw(self.player)

        # set sound volume
        self.set_sound_value()

        # play walk sound
        self.play_walking_sound()
        
        if self.is_menu_open:
            self.eventctrl.is_event_listening = False # avoid z/return/space problem

            # run menu
            param = self.menu.run()

            self.is_menu_open = not param.close_menu

            if param.save_load_path is not None:
                self.stop_bgm_and_bgs()
                return param

        elif self.is_saving:
            self.is_menu_listening = False # avoid esc problem

            # run save
            param = self.savepage.run()

            self.eventctrl.is_open_saving = not param

        else:
            # run events
            param = self.eventctrl.run()

            # update sprites (including player)
            self.visible_sprites.update()

            # listen to menu
            self.menu_listener()

            # change map
            if isinstance(param, ChangeMapParam):
                self.stop_bgm_and_bgs()

            return param

        return None

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

    def custom_draw(self,player):

        # getting the offset 
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

