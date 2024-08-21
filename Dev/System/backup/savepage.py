import pygame
import json

from settings import *
from support import draw_text

class SavePage:
    def __init__(self, menu, player) -> None:
        self.menu = menu
        self.save_data = menu.save_data
        self.player = player

        self.display_surface = pygame.display.get_surface()

        self.background_surf = pygame.surface.Surface((WIDTH, HEIGTH))
        self.background_surf.fill((0,0,128))

        # select info
        self.focus = 0
        self.is_key_listening = False

    def save(self, file_path):
        player_status = {
            "pos": [round(self.player.rect.x / TILESIZE), round(self.player.rect.y / TILESIZE)], 
            "status": self.player.status
        }
        self.save_data["player-status"] = player_status
        with open(file_path, "w", encoding = "utf8") as file:
            json.dump(self.save_data, file, indent = 4)
        print("save data to {}".format(file_path))

    def listener(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] or keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_ESCAPE]:
            if self.is_key_listening:
                self.is_key_listening = False
                if keys[pygame.K_z] or keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                    self.menu.choose_sound.play()
                    file_path = SAVE_FILE_PATH.format(str(self.focus + 1))
                    self.save(file_path)
                    return True
                elif keys[pygame.K_UP]:
                    self.menu.switch_sound.play()
                    self.focus = (self.focus - 1) % 5
                elif keys[pygame.K_DOWN]:
                    self.menu.switch_sound.play()
                    self.focus = (self.focus + 1) % 5
                elif keys[pygame.K_ESCAPE]:
                    self.menu.choose_sound.play()
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
        """return whether to close saving"""
        escape = self.listener()
        self.draw()
        return escape

