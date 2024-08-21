from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mapctrl import MapCtrl

import json
import os

import pygame

from key import KeyPress, KeySettings, code_key_dict
from settings import *
from sound import choose_sound, switch_sound, BGM, BGS, SE
from support import draw_text

class Menu:
    def __init__(self, mapctrl: MapCtrl) -> None:
        # load player settings
        self.load_settings()

        self.mapctrl = mapctrl

        self.setting_data = mapctrl.setting_data

        # save data
        self.save_data = mapctrl.save_data

        # get display surface
        self.display_surface = pygame.display.get_surface()

        # load menu background
        self.background_surf = pygame.image.load("../Graphics/layer/menu_background.png")

        # choose surf
        self.choose_surf = pygame.surface.Surface((156,52)).convert_alpha()
        self.choose_surf.fill((255,255,255))
        self.choose_surf.set_alpha(128)
        
        self.is_key_listening = False

        # focus section
        self.focus_section = 0
        self.select_section = None

        # load file
        self.lf = LoadFileSect(self)

        # setting
        self.st = SettingSect(self)

    def load_settings(self):
        with open(SETTING_FILE_PATH, mode = "r") as file:
            data = json.load(file)
        self.setting_data = data

    def set_sound_volume(self):
        BGM.set_global_volume(self.setting_data["volume"]["BGM"])
        BGS.set_global_volume(self.setting_data["volume"]["BGS"])
        SE.set_global_volume(self.setting_data["volume"]["SE"])

    def save_settings(self):
        with open(SETTING_FILE_PATH, mode = "r") as file:
            json.dump(file, indent = 4)

    def section_listener(self):
        keys = KeyPress.keys
        keys_int = (KeySettings.confirm_1, KeySettings.confirm_2, 
                    KeySettings.menu_1, KeySettings.menu_2, 
                    KeySettings.cancel_1, KeySettings.cancel_2, 
                    KeySettings.up, KeySettings.down)
        if any(keys[i] for i in keys_int):
            if self.is_key_listening:
                self.is_key_listening = False
                if keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2] or keys[KeySettings.right]:
                    self.select_section = self.focus_section
                    choose_sound.play()
                    self.lf.load_file_list()
                elif keys[KeySettings.up]:
                    self.focus_section = (self.focus_section - 1) % 3
                    switch_sound.play()
                elif keys[KeySettings.down]:
                    self.focus_section = (self.focus_section + 1) % 3
                    switch_sound.play()
                elif keys[KeySettings.menu_1] or keys[KeySettings.menu_2] or keys[KeySettings.cancel_1] or keys[KeySettings.cancel_2]:
                    self.mapctrl.level.is_menu_open = False
                    choose_sound.play()
        else:
            self.is_key_listening = True

    def section_draw(self):
        # display focus rect
        pos = (20, 20 + 61 * self.focus_section)
        self.display_surface.blit(self.choose_surf, pos)

    def reset_param(self):
        self.is_key_listening = False
        self.focus_section = 0
        self.select_section = None

    def run(self):
        # display background
        self.display_surface.blit(self.background_surf, (0,0))

        if self.select_section is None:
            self.section_listener()
            self.section_draw()
        elif self.select_section == 0:
            self.mapctrl.level.is_menu_open = False
        elif self.select_section == 1:
            self.section_draw()
            self.lf.run()
        elif self.select_section == 2:
            self.section_draw()
            self.st.run()
        
        if not self.mapctrl.level.is_menu_open:
            self.reset_param()


class LoadFileSect:
    def __init__(self, menu: Menu) -> None:
        self.menu = menu
        self.pos = (214, 24)
        self.focus = 0
        self.load_file_list()
        self.is_key_listening = False

    def load_file_list(self):
        self.file_list = []
        self.file_list = []
        for i in range(5):
            if os.path.isfile(f"../data/save/file{i+1}.json"):
                self.file_list.append(i)

    def listener(self):
        keys = KeyPress.keys
        if keys[KeySettings.up] or keys[KeySettings.down] or keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2] or keys[KeySettings.cancel_1] or keys[KeySettings.cancel_2] or keys[KeySettings.left]:
            if self.is_key_listening:
                self.is_key_listening = False
                if keys[KeySettings.up]:
                    self.focus = (self.focus - 1) % len(self.file_list)
                    switch_sound.play()
                elif keys[KeySettings.down]:
                    self.focus = (self.focus + 1) % len(self.file_list)
                    switch_sound.play()
                elif keys[KeySettings.cancel_1] or keys[KeySettings.cancel_2] or keys[KeySettings.left]:
                    self.menu.select_section = None
                    choose_sound.play()
                elif keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2]:
                    self.menu.mapctrl.level.is_menu_open = False
                    self.menu.mapctrl.level.stop_bgm_and_bgs()
                    self.menu.mapctrl.reload_from_save_data("../data/save/file" + str(self.file_list[self.focus] + 1) + ".json")
                    choose_sound.play()
        else:
            self.is_key_listening = True

    def draw(self):
        surf = pygame.surface.Surface((740, HEIGTH - 48))
        for index, i in enumerate(self.file_list):
            if self.focus != index:
                choice = pygame.image.load("../Graphics/layer/choice.png")
            else:
                choice = pygame.image.load("../Graphics/layer/choice_focus.png")
            draw_text(choice, f"file{i+1}", 22, None, None)
            surf.blit(choice, (10, 10 + 70 * index))
        self.menu.display_surface.blit(surf, self.pos)

    def run(self):
        self.listener()
        self.draw()

class SettingSect:
    def __init__(self, menu: Menu) -> None:
        self.menu = menu
        self.ori_pos = [214, 24]
        self.pos = [214, 24]
        self.focus = 0
        self.is_key_listening = False

        self.subsect = 0

        self.keys_sect_select = None
    
    def volume_subsect_listener(self):
        keys = KeyPress.keys
        if keys[KeySettings.up] or keys[KeySettings.down] or keys[KeySettings.left] or keys[KeySettings.right] \
            or keys[KeySettings.cancel_1] or keys[KeySettings.cancel_2] or keys[KeySettings.menu_1] or keys[KeySettings.menu_2]:
            if self.is_key_listening:
                self.is_key_listening = False
                if keys[KeySettings.up]:
                    self.focus = max(self.focus - 1, 0)
                    switch_sound.play()
                elif keys[KeySettings.down]:
                    self.focus += 1
                    if self.focus == 3:
                        self.focus = 0
                        self.subsect = 1
                    switch_sound.play()
                elif keys[KeySettings.cancel_1] or keys[KeySettings.cancel_2] or keys[KeySettings.menu_1] or keys[KeySettings.menu_2]:
                    self.menu.select_section = None
                    choose_sound.play()
                elif keys[KeySettings.left]:
                    if self.focus == 0:
                        self.menu.setting_data["volume"]["BGM"] = max(self.menu.setting_data["volume"]["BGM"] - 0.05, 0)
                    elif self.focus == 1:
                        self.menu.setting_data["volume"]["BGS"] = max(self.menu.setting_data["volume"]["BGS"] - 0.05, 0)
                    elif self.focus == 2:
                        self.menu.setting_data["volume"]["SE"] = max(self.menu.setting_data["volume"]["SE"] - 0.05, 0)
                    self.menu.setting_data.save_to()
                    self.menu.set_sound_volume()
                    choose_sound.play()
                elif keys[KeySettings.right]:
                    if self.focus == 0:
                        self.menu.setting_data["volume"]["BGM"] = min(self.menu.setting_data["volume"]["BGM"] + 0.05, 1)
                    elif self.focus == 1:
                        self.menu.setting_data["volume"]["BGS"] = min(self.menu.setting_data["volume"]["BGS"] + 0.05, 1)
                    elif self.focus == 2:
                        self.menu.setting_data["volume"]["SE"] = min(self.menu.setting_data["volume"]["SE"] + 0.05, 1)
                    self.menu.setting_data.save_to()
                    self.menu.set_sound_volume()
                    choose_sound.play()
        else:
            self.is_key_listening = True

    def keys_subsect_listener(self):
        keys = KeyPress.keys
        if keys[KeySettings.up] or keys[KeySettings.down] or keys[KeySettings.left] or keys[KeySettings.right] \
            or keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2] \
            or keys[KeySettings.cancel_1] or keys[KeySettings.cancel_2] or keys[KeySettings.menu_1] or keys[KeySettings.menu_2]:
            if self.is_key_listening:
                self.is_key_listening = False
                if keys[KeySettings.up]:
                    self.focus -= 1
                    if self.focus == -1:
                        self.focus = 2
                        self.subsect = 0
                    switch_sound.play()
                elif keys[KeySettings.down]:
                    self.focus = min(self.focus + 1, 13)
                    switch_sound.play()
                elif keys[KeySettings.cancel_1] or keys[KeySettings.cancel_2] or keys[KeySettings.menu_1] or keys[KeySettings.menu_2]:
                    self.menu.select_section = None
                    choose_sound.play()
                elif keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2]:
                    self.keys_sect_select = self.focus
                    choose_sound.play()
        else:
            self.is_key_listening = True

    def setting_key_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.is_key_listening = False
                key_value = event.key
                KeySettings.set_key_by_idx(self.focus, key_value)
                self.menu.setting_data.save_to()
                self.keys_sect_select = None
                choose_sound.play()

    def listener(self):
        if self.keys_sect_select is None:
            if self.subsect == 0:
                self.volume_subsect_listener()
            elif self.subsect == 1:
                self.keys_subsect_listener()
        else:
            self.setting_key_listener()

    def draw(self):
        count = 0
        surf = pygame.surface.Surface((740, 2048))

        y_pos_list = []

        # volume
        draw_text(surf, "Volume", 30, 10, 10 + 70 * count)
        count += 1
        for idx, key in enumerate(("BGM", "BGS", "SE")):
            value = self.menu.setting_data["volume"][key]
            color = (255, 255, 255) if self.subsect != 0 or self.focus != idx else (255, 255, 0)
            draw_text(surf, key, 22, 30, 10 + 70 * count, color)
            surf.blit(BarSurf(value).surf, (90, 15 + 70 * count))
            y_pos_list.append(10 + 70 * count)
            count += 1
        
        # keys settings
        draw_text(surf, "Keys", 30, 10, 10 + 70 * count)
        count += 1
        for i in range(14):
            color1 = (255, 255, 255) if self.subsect != 1 or self.focus != i else (255, 255, 0)
            draw_text(surf, KeySettings.keys_list[i], 22, 30, 15 + 70 * count, color1)
            color2 = (255, 255, 255) if self.keys_sect_select != self.focus or self.focus != i else (255, 255, 0)
            draw_text(surf, pygame.key.name(KeySettings.get_key_by_idx(i)), 22, 200, 15 + 70 * count, color2)
            y_pos_list.append(10 + 70 * count)
            count += 1

        if self.subsect >= 1:
            self.pos[1] = self.ori_pos[1] - self.focus * 70
        else:
            self.pos = self.ori_pos.copy()

        self.menu.display_surface.blit(surf, self.pos)

    def run(self):
        self.listener()
        self.draw()

class BarSurf:
    def __init__(self, ratio) -> None:
        self.ratio = ratio
        self.surf = pygame.image.load("../Graphics/layer/bar.png")
        self.length = self.surf.get_width()
        self.rect = pygame.surface.Surface((5, self.surf.get_height()))
        self.rect.fill((255,255,255))
        self.surf.blit(self.rect, ((self.length - 5) * self.ratio, 0))
    
