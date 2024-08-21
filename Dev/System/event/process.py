from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mapctrl import MapCtrl
    from event.commonevent import CommonEvent, Command

import pygame

from key import KeyPress, KeySettings
from settings import *
from sound import SE, choose_sound, switch_sound
from support import draw_text

class Process:
    def __init__(self, mapctrl: MapCtrl, commonevent: CommonEvent, lock_player: bool) -> None:
        self.mapctrl = mapctrl
        self.commonevent = commonevent
        self.lock_player = lock_player
        self.is_finished = False
    
    def default_run(self):
        self.commonevent.lock_player = self.commonevent.lock_player or self.lock_player

class ChangeMap(Process):
    def __init__(self, mapctrl: MapCtrl, commonevent: CommonEvent, lock_player: bool, 
                 to_map, exit_sound_path, enter_sound_path, player_status) -> None:
        super().__init__(mapctrl, commonevent, lock_player)
        self.to_map = to_map
        self.exit_sound = None if exit_sound_path is None else SE(exit_sound_path)
        self.enter_sound = None if enter_sound_path is None else SE(enter_sound_path)
        self.player_status = player_status

        self.display_surface = mapctrl.level.display_surface
        self.alpha = 0
        self.surface = pygame.Surface((WIDTH, HEIGTH))

        self.is_exiting = True

        if self.exit_sound is not None:
            self.exit_sound.play()
    
    def change_map(self):
        self.mapctrl.change_map_to(self.to_map, self.player_status)
        self.is_exiting = False

        if self.enter_sound is not None:
            self.enter_sound.play()
        self.is_finished = True

    def run(self):
        self.default_run()
        if self.is_exiting:
            speed = 4
            self.alpha += speed

            if self.alpha > 255:
                self.surface.set_alpha(255)
                self.display_surface.blit(self.surface, (0,0))
                self.change_map()
                return 
            
            self.surface.set_alpha(self.alpha)
            self.display_surface.blit(self.surface, (0,0))
        else:
            pass 

class ShowText(Process):
    def __init__(self, mapctrl: MapCtrl, commonevent: CommonEvent, lock_player: bool, 
                 script_ranges: list) -> None:
        super().__init__(mapctrl, commonevent, lock_player)
        self.display_surface = self.mapctrl.level.display_surface
        self.script_ranges = script_ranges

        self.dialog_surf = pygame.image.load("../Graphics/layer/dialog_box.png").convert_alpha()
        self.dialog_surf.set_alpha(230)
        self.dialog_topleft = ((WIDTH - self.dialog_surf.get_width()) // 2, HEIGTH - self.dialog_surf.get_height())
        self.triangle_surf = pygame.image.load("../Graphics/layer/triangle.png").convert_alpha()
        self.triangle_topleft = ((WIDTH - self.triangle_surf.get_width()) // 2, HEIGTH - self.triangle_surf.get_height() - 5)
        self.dialog_surf.set_alpha(230)

        self.script_list = []
        for r in script_ranges:
            start, end = map(int, r.split("-"))
            self.script_list += [f"message_{i}" for i in range(start, end + 1)]
        self.sound = SE("../Audio/SE/subtitle_run.ogg")

        self.script_count = 0
        self.script_chr_count = 0
        self.is_key_listening = False
    
    def run(self):
        self.default_run()

        self.display_surface.blit(self.dialog_surf, self.dialog_topleft)
        
        # script content
        script_content = self.mapctrl.script_data[self.script_list[self.script_count]]
        speaker_name = script_content.get("speakerName")
        content = script_content["text"]

        # play/stop sound
        if self.script_chr_count == 0:
            self.sound.play(-1)
        elif self.script_chr_count >= len(content) + 1:
            self.sound.stop()

        # text animate
        speed = 0.3
        self.script_chr_count += speed
        if self.script_chr_count >= len(content) + 1:
            self.script_chr_count = len(content) + 1
        draw_content = content[:int(self.script_chr_count)]
        # draw text
        lines = draw_content.split("\n")
        x = self.dialog_topleft[0] + 40
        y = self.dialog_topleft[1]
        if speaker_name is not None:
            draw_text(self.display_surface, f"【{speaker_name}】", 30, x, y + 20)
        else:
            y -= 30
        for index, line in enumerate(lines):
            draw_text(self.display_surface, line, 22, x + 20, y + 60 + index*30)

        # draw triangle
        if self.script_chr_count == len(content) + 1:
            self.display_surface.blit(self.triangle_surf, self.triangle_topleft)

        # next text
        keys = KeyPress.keys
        if keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2] or keys[KeySettings.cancel_1] or keys[KeySettings.cancel_2]:
            if self.is_key_listening:
                self.is_key_listening = False
                if self.script_chr_count < len(content) + 1:
                    self.script_chr_count = len(content) + 1
                    self.sound.stop()
                else:
                    self.script_count += 1
                    self.script_chr_count = 0
                    if self.script_count >= len(self.script_list):
                        self.sound.stop()
                        self.is_finished = True
                        return
        else:
            self.is_key_listening = True

class ShowChoices(Process):
    def __init__(self, mapctrl: MapCtrl, commonevent: CommonEvent, lock_player: bool, 
                 script_ranges: list[str], after: dict[str, list], command: Command) -> None:
        super().__init__(mapctrl, commonevent, lock_player)
        self.command = command
        self.script_ranges = script_ranges
        self.after = after
        self.display_surface = self.mapctrl.level.display_surface

        self.choice_msg_list = []
        for r in script_ranges:
            start, end = map(int, r.split("-"))
            self.choice_msg_list += [f"{i}" for i in range(start, end + 1)]
        
        # load image
        surf = pygame.image.load("../Graphics/layer/choice.png").convert_alpha()

        # calculate position
        w, h = surf.get_width(), surf.get_height()
        self.topleft_list = []
        x = (WIDTH - w) // 2
        for index in range(len(self.choice_msg_list))[::-1]:
            y = HEIGTH - h - 60 * index - 20
            self.topleft_list.append((x, y))

        self.focused_choice = 0
        self.is_key_listening = False

        self.after_contents = None

    def run(self):
        self.default_run()

        keys = KeyPress.keys
        if keys[KeySettings.up] or keys[KeySettings.down] or keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2]:
            if self.is_key_listening:
                self.is_key_listening = False
                if keys[KeySettings.up]:
                    self.focused_choice = (self.focused_choice - 1) % len(self.choice_msg_list)
                    switch_sound.play()
                if keys[KeySettings.down]:
                    self.focused_choice = (self.focused_choice + 1) % len(self.choice_msg_list)
                    switch_sound.play()
                if keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2]:
                    choose_sound.play()
                    choice = self.choice_msg_list[self.focused_choice]
                    contents = self.after[choice]
                    self.is_finished = True
                    self.command.insert_contents_and_init(contents)
        else:
            self.is_key_listening = True

        for index, choice in enumerate(self.choice_msg_list):
            text = self.mapctrl.script_data["choice_" + choice]["text"]
            pos = self.topleft_list[index]
            if index == self.focused_choice:
                surf = pygame.image.load("../Graphics/layer/choice_focus.png").convert_alpha()
                surf.set_alpha(230)
                draw_text(surf, text, 22, None, None)
                self.display_surface.blit(surf, pos)
            else:
                surf = pygame.image.load("../Graphics/layer/choice.png").convert_alpha()
                surf.set_alpha(230)
                draw_text(surf, text, 22, None, None)
                self.display_surface.blit(surf, pos)

class ShowPicture(Process):
    def __init__(self, mapctrl: MapCtrl, commonevent: CommonEvent, lock_player: bool, 
                 filepath: str, is_alpha_animate: bool | None) -> None:
        super().__init__(mapctrl, commonevent, lock_player)
        self.display_surface = self.mapctrl.level.display_surface

        self.img = pygame.image.load(filepath).convert_alpha()
        w, h = self.img.get_width(), self.img.get_height()
        x = (WIDTH - w) // 2
        y = int(HEIGTH*0.4) - (h // 2)
        self.pos = (x, y)
        self.is_key_listening = False
        if is_alpha_animate is not None:
            if is_alpha_animate:
                self.alpha = 0
            else:
                self.alpha = 255
        else:
            self.alpha = 255

    def run(self):
        self.default_run()
        
        # alpha animate
        speed = 4
        self.alpha += speed
        if self.alpha > 255:
            self.alpha = 255
        self.img.set_alpha(self.alpha)

        # get key pressed
        keys = KeyPress.keys
        if keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2]:
            if self.is_key_listening:
                self.is_key_listening = False
                if self.alpha < 255:
                    self.alpha = 255
                else:
                    self.is_finished = True
        else:
            self.is_key_listening = True

        self.display_surface.blit(self.img, self.pos)

class GameOver(Process):
    def __init__(self, mapctrl: MapCtrl, commonevent: CommonEvent, lock_player: bool, 
                 script_ranges: list[str] | None, play_sound: str | None) -> None:
        super().__init__(mapctrl, commonevent, lock_player)
        self.display_surface = mapctrl.level.display_surface
        self.image = pygame.image.load("../Graphics/layer/game_over.png")
        
        self.script_ranges = script_ranges
        self.play_sound = None if play_sound is None else SE(play_sound)

        self.play_sound.play() if self.play_sound is not None else None

        self.mapctrl.level.stop_bgm_and_bgs()

        if script_ranges is not None:
            self.dialog_surf = pygame.surface.Surface((960, 225)).convert_alpha()
            self.dialog_surf.fill((0,0,0))
            self.dialog_surf.set_alpha(128)
            self.dialog_topleft = (0, (HEIGTH - self.dialog_surf.get_height()) // 2)

            self.script_list = []
            for r in script_ranges:
                start, end = map(int, r.split("-"))
                self.script_list += [f"message_{i}" for i in range(start, end + 1)]
            self.sound = SE("../Audio/SE/subtitle_run.ogg")

            self.script_count = 0
            self.script_chr_count = 0
            self.is_key_listening = False

    def run_script(self):

        self.display_surface.blit(self.dialog_surf, self.dialog_topleft)
        
        # script content
        script_content = self.mapctrl.script_data[self.script_list[self.script_count]]
        content = script_content["text"]

        # play/stop sound
        if self.script_chr_count == 0:
            self.sound.play(-1)
        elif self.script_chr_count >= len(content) + 1:
            self.sound.stop()

        # text animate
        speed = 0.3
        self.script_chr_count += speed
        if self.script_chr_count >= len(content) + 1:
            self.script_chr_count = len(content) + 1
        draw_content = content[:int(self.script_chr_count)]
        # draw text
        lines = draw_content.split("\n")
        for line in lines:
            draw_text(self.display_surface, line, 22, None, None)

        # draw triangle
        # if self.script_chr_count == len(content) + 1:
        #     self.display_surface.blit(self.triangle_surf, self.triangle_topleft)

        # next text
        keys = KeyPress.keys
        if keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2]:
            if self.is_key_listening:
                self.is_key_listening = False
                if self.script_chr_count < len(content) + 1:
                    self.script_chr_count = len(content) + 1
                    self.sound.stop()
                else:
                    self.script_count += 1
                    self.script_chr_count = 0
                    if self.script_count >= len(self.script_list):
                        self.sound.stop()
                        self.script_ranges = None
                        return
        else:
            self.is_key_listening = True

    def run(self):
        self.default_run()

        self.display_surface.blit(self.image, (0,0))

        if self.script_ranges is not None:
            self.run_script()
        else:
            self.mapctrl.level.forced_menu_listening = True

class OpenDarkCover(Process):
    def __init__(self, mapctrl: MapCtrl, commonevent: CommonEvent, lock_player: bool, 
                 size: int, is_animate: bool | None) -> None:
        super().__init__(mapctrl, commonevent, lock_player)
        self.is_animate = False if is_animate is None else is_animate
        self.surf = pygame.image.load(f"../Graphics/layer/dark_cover_{size}.png").convert_alpha()
        self.alpha = 0 if self.is_animate else 255

    def run(self):
        self.default_run()

        speed = 4
        self.alpha += speed
        
        if self.alpha >= 255:
            self.alpha = 255
            self.is_finished = True
        
        self.surf.set_alpha(self.alpha)
        self.mapctrl.level.dark_cover_surf = self.surf

class CloseDarkCover(Process):
    def __init__(self, mapctrl: MapCtrl, commonevent: CommonEvent, lock_player: bool, 
                 is_animate: bool | None) -> None:
        super().__init__(mapctrl, commonevent, lock_player)
        self.is_animate = False if is_animate is None else is_animate
        self.surf = self.mapctrl.level.dark_cover_surf
        self.alpha = 255 if self.is_animate else 0

    def run(self):
        self.default_run()

        speed = 4
        self.alpha -= speed
        
        if self.alpha <= 0:
            self.alpha = 0
            self.mapctrl.level.dark_cover_surf = None
            self.is_finished = True
            return 
        
        self.surf.set_alpha(self.alpha)
        self.mapctrl.level.dark_cover_surf = self.surf

