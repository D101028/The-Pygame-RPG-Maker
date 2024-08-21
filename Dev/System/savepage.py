from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mapctrl import MapCtrl

import pygame

from key import KeyPress, KeySettings
from settings import *
from sound import choose_sound, switch_sound
from support import draw_text

class SavePage:
    def __init__(self, mapctrl: MapCtrl) -> None:
        self.mapctrl = mapctrl

        self.menu = mapctrl.menu
        self.save_data = mapctrl.save_data

        self.display_surface = pygame.display.get_surface()

        self.background_surf = pygame.surface.Surface((WIDTH, HEIGTH))
        self.background_surf.fill((0,0,128))

        # select info
        self.focus = 0
        self.is_key_listening = False

    def save(self, file_path):
        player = self.mapctrl.level.player
        player_status = {
            "pos": [round(player.rect.x / TILESIZE), round(player.rect.y / TILESIZE)], 
            "status": player.status, 
            "map": self.mapctrl.proceeding_map
        }
        self.save_data.save_to(file_path, player_status)

    def listener(self):
        keys = KeyPress.keys
        if keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2] \
            or keys[KeySettings.cancel_1] or keys[KeySettings.cancel_2] \
            or keys[KeySettings.up] or keys[KeySettings.down]:
            if self.is_key_listening:
                self.is_key_listening = False
                if keys[KeySettings.confirm_1] or keys[KeySettings.confirm_2]:
                    choose_sound.play()
                    file_path = SAVE_FILE_PATH.format(str(self.focus + 1))
                    self.save(file_path)
                    return True
                elif keys[KeySettings.up]:
                    switch_sound.play()
                    self.focus = (self.focus - 1) % 5
                elif keys[KeySettings.down]:
                    switch_sound.play()
                    self.focus = (self.focus + 1) % 5
                elif keys[KeySettings.cancel_1] or keys[KeySettings.cancel_2]:
                    choose_sound.play()
                    return True
        else:
            self.is_key_listening = True
        return False

    def draw(self):
        """return whether to close saving"""
        self.display_surface.blit(self.background_surf, (0,0))
        
        # blit choices
        surf = pygame.surface.Surface((120, 60))
        surf.fill((255,255,255))
        draw_text(surf, "save", 22, None, None, (0,0,0))
        pos = ((WIDTH - surf.get_width()) // 2, HEIGTH // 2 - 210)
        self.display_surface.blit(surf, pos)
        for i in range(5):
            if self.focus != i:
                surf = pygame.image.load("../Graphics/layer/choice.png")
                draw_text(surf, f"file{i+1}", 22, None, None)
                pos = ((WIDTH - surf.get_width()) // 2, HEIGTH // 2 - (2 - i) * 70)
                self.display_surface.blit(surf, pos)
            else:
                surf = pygame.image.load("../Graphics/layer/choice_focus.png")
                draw_text(surf, f"file{i+1}", 22, None, None)
                pos = ((WIDTH - surf.get_width()) // 2, HEIGTH // 2 - (2 - i) * 70)
                self.display_surface.blit(surf, pos)

    def run(self) -> bool:
        escape = self.listener()
        self.draw()
        if escape:
            self.mapctrl.level.is_saving = False

