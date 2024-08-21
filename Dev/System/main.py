import pygame
import sys

from debug import debug
from mapctrl import MapCtrl
from settings import *

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()

        # map contral
        self.mapctrl = MapCtrl()

        # sound 
        pygame.mixer.init()

        # show fps
        self.is_show_fps = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKQUOTE: # show fps
                        self.is_show_fps = not self.is_show_fps

            self.screen.fill(BLACK_COLOR)
            self.mapctrl.run()
            if self.is_show_fps:
                debug(f"{self.clock.get_fps(): .2f}")
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()