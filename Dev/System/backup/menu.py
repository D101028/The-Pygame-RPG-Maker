import pygame
import json
import os

from settings import *
from support import draw_text

class MenuReturnParam:
    def __init__(self) -> None:
        self.close_menu = False
        self.save_load_path = None

class Menu:
    def __init__(self, save_data) -> None:
        # load player settings
        self.load_settings()

        # save data
        self.save_data = save_data

        # get display surface
        self.display_surface = pygame.display.get_surface()

        # load menu background
        self.background_surf = pygame.image.load("../Graphics/layer/menu_background.png")

        # sound
        self.switch_sound = pygame.mixer.Sound("../Audio/SE/yisell_sound.ogg")
        self.choose_sound = pygame.mixer.Sound("../Audio/SE/choose_sound.ogg")
        self.set_sound_volume()

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

        # MenuReturnParam
        self.menu_return_param = MenuReturnParam()

    def load_settings(self):
        with open(SETTING_FILE_PATH, mode = "r") as file:
            data = json.load(file)
        self.settings = data

    def set_sound_volume(self):
        self.switch_sound.set_volume(self.settings["volume"]["SE"])
        self.choose_sound.set_volume(self.settings["volume"]["SE"])

    def save_settings(self):
        with open(SETTING_FILE_PATH, mode = "r") as file:
            json.dump(file, indent = 4)

    def section_listener(self):
        keys = pygame.key.get_pressed()
        keys_int = (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_ESCAPE)
        if any(keys[i] for i in keys_int):
            if self.is_key_listening:
                self.is_key_listening = False
                if keys[pygame.K_RETURN] or keys[pygame.K_z] or keys[pygame.K_SPACE] or keys[pygame.K_RIGHT]:
                    self.select_section = self.focus_section
                    self.choose_sound.play()
                    self.lf.load_file_list()
                elif keys[pygame.K_UP]:
                    self.focus_section = (self.focus_section - 1) % 3
                    self.switch_sound.play()
                elif keys[pygame.K_DOWN]:
                    self.focus_section = (self.focus_section + 1) % 3
                    self.switch_sound.play()
                elif keys[pygame.K_ESCAPE]:
                    self.menu_return_param.close_menu = True
                    self.choose_sound.play()
        else:
            self.is_key_listening = True

    def section_draw(self):
        # display focus rect
        pos = (20, 20 + 61 * self.focus_section)
        self.display_surface.blit(self.choose_surf, pos)

    def reset_param(self):
        self.menu_return_param = MenuReturnParam()
        self.is_key_listening = False
        self.focus_section = 0
        self.select_section = None

    def run(self):
        """return MenuReturnParam"""
        # display background
        self.display_surface.blit(self.background_surf, (0,0))

        if self.select_section is None:
            self.section_listener()
            self.section_draw()
        elif self.select_section == 0:
            self.menu_return_param.close_menu = True
        elif self.select_section == 1:
            self.section_draw()
            self.lf.run()
        elif self.select_section == 2:
            self.section_draw()
            self.st.run()

        param = self.menu_return_param
        
        if param.close_menu:
            self.reset_param()

        return param

class LoadFileSect:
    def __init__(self, menu_class: Menu) -> None:
        self.menu_class = menu_class
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RETURN] or keys[pygame.K_z] or keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE] or keys[pygame.K_LEFT]:
            if self.is_key_listening:
                self.is_key_listening = False
                if keys[pygame.K_UP]:
                    self.focus = (self.focus - 1) % len(self.file_list)
                    self.menu_class.switch_sound.play()
                elif keys[pygame.K_DOWN]:
                    self.focus = (self.focus + 1) % len(self.file_list)
                    self.menu_class.switch_sound.play()
                elif keys[pygame.K_ESCAPE] or keys[pygame.K_LEFT]:
                    self.menu_class.select_section = None
                    self.menu_class.choose_sound.play()
                elif keys[pygame.K_RETURN] or keys[pygame.K_z] or keys[pygame.K_SPACE]:
                    self.menu_class.menu_return_param.close_menu = True
                    self.menu_class.menu_return_param.save_load_path = "../data/save/file" + str(self.file_list[self.focus] + 1) + ".json"
                    self.menu_class.choose_sound.play()
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
        self.menu_class.display_surface.blit(surf, self.pos)

    def run(self):
        self.listener()
        self.draw()

class SettingSect:
    def __init__(self, menu_class: Menu) -> None:
        self.menu_class = menu_class
        self.pos = (214, 24)
        self.focus = 0
        self.is_key_listening = False
    
    def save_settings(self):
        with open(SETTING_FILE_PATH, mode = "w") as file:
            json.dump(self.menu_class.settings, file, indent = 4)

    def listener(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_ESCAPE]:
            if self.is_key_listening:
                self.is_key_listening = False
                if keys[pygame.K_UP]:
                    self.focus = (self.focus - 1) % 3
                    self.menu_class.switch_sound.play()
                elif keys[pygame.K_DOWN]:
                    self.focus = (self.focus + 1) % 3
                    self.menu_class.switch_sound.play()
                elif keys[pygame.K_ESCAPE]:
                    self.menu_class.select_section = None
                    self.menu_class.choose_sound.play()
                elif keys[pygame.K_LEFT]:
                    if self.focus == 0:
                        self.menu_class.settings["volume"]["BGM"] = max(self.menu_class.settings["volume"]["BGM"] - 0.05, 0)
                    elif self.focus == 1:
                        self.menu_class.settings["volume"]["BGS"] = max(self.menu_class.settings["volume"]["BGS"] - 0.05, 0)
                    elif self.focus == 2:
                        self.menu_class.settings["volume"]["SE"] = max(self.menu_class.settings["volume"]["SE"] - 0.05, 0)
                    self.save_settings()
                    self.menu_class.set_sound_volume()
                    self.menu_class.choose_sound.play()
                elif keys[pygame.K_RIGHT]:
                    if self.focus == 0:
                        self.menu_class.settings["volume"]["BGM"] = max(self.menu_class.settings["volume"]["BGM"] + 0.05, 0)
                    elif self.focus == 1:
                        self.menu_class.settings["volume"]["BGS"] = max(self.menu_class.settings["volume"]["BGS"] + 0.05, 0)
                    elif self.focus == 2:
                        self.menu_class.settings["volume"]["SE"] = max(self.menu_class.settings["volume"]["SE"] + 0.05, 0)
                    self.save_settings()
                    self.menu_class.set_sound_volume()
                    self.menu_class.choose_sound.play()
        else:
            self.is_key_listening = True

    def draw(self):
        count = 0
        surf = pygame.surface.Surface((740, HEIGTH - 48))

        y_pos_list = []

        # volume
        draw_text(surf, "Volume", 30, 10, 10 + 70 * count)
        count += 1
        for key in ("BGM", "BGS", "SE"):
            value = self.menu_class.settings["volume"][key]
            draw_text(surf, key, 22, 30, 10 + 70 * count)
            surf.blit(BarSurf(value).surf, (90, 15 + 70 * count))
            y_pos_list.append(10 + 70 * count)
            count += 1
        
        # draw focus
        draw_text(surf, "**", 22, 10, y_pos_list[self.focus])

        self.menu_class.display_surface.blit(surf, self.pos)

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
    
