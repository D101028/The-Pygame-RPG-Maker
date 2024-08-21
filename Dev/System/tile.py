import pygame 

from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE,TILESIZE)), event_id = None, ground_id = None):
        super().__init__(groups)
        self.sprite_type = sprite_type
        if sprite_type == 'object':
            height = surface.get_size()[1]
            width = surface.get_size()[0]
            y_offset = -int(height * 0.3125) if height <= 128 else -int(height * 0.5)
            x_offset = 0 if width <= 128 else -int(width * 0.3)
            self.image = surface
            self.rect = self.image.get_rect(bottomleft = (pos[0], pos[1] + TILESIZE))
            self.hitbox = self.rect.inflate(x_offset, y_offset)
            if height > 128:
                self.hitbox.y += height * 0.1
        elif sprite_type == 'event':
            y_offset = HITBOX_OFFSET[sprite_type]
            self.image = surface
            self.event_id = event_id
            self.rect = self.image.get_rect(topleft = pos)
            self.hitbox = self.rect.inflate(0, y_offset)
        elif sprite_type == 'groundtype':
            self.image = surface
            self.ground_id = ground_id
            self.rect = self.image.get_rect(topleft = pos)
            self.hitbox = self.rect.inflate(0, 0)
        else:
            y_offset = HITBOX_OFFSET[sprite_type]
            self.image = surface
            self.rect = self.image.get_rect(topleft = pos)
            self.hitbox = self.rect.inflate(0, y_offset)

