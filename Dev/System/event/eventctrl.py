from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mapctrl import MapCtrl

import pygame

from event.commonevent import CommonEvent
from settings import *

class EventCtrl:
    def __init__(self, mapctrl: MapCtrl) -> None:
        self.mapctrl = mapctrl
        self.map_data = mapctrl.map_data

        self.extract_id_events()

        self.extract_background_events()

        self.is_event_listening = False

    def extract_id_events(self):
        self.commonevents: list[CommonEvent] = []
        for index, event_data in enumerate(self.map_data["events"]):
            self.commonevents.append(CommonEvent(self.mapctrl, event_data, index))

    def extract_background_events(self):
        self.bg_commonevents: list[CommonEvent] = []
        for event_data in self.map_data["background-events"]:
            self.bg_commonevents.append(CommonEvent(self.mapctrl, event_data, None))

    def event_sprite_collision_judge(self, event_sprite):
        player = self.mapctrl.level.player
        trigger = False
        if "up" in player.status:
            trigger = -TILESIZE//2 <= player.hitbox.topleft[1] - event_sprite.hitbox.bottomleft[1] <= TILESIZE//2 and event_sprite.hitbox.bottomleft[0] <= player.hitbox.center[0] <= event_sprite.hitbox.bottomright[0]
        elif "down" in player.status:
            trigger = -TILESIZE//2 <= event_sprite.hitbox.topleft[1] - player.hitbox.bottomleft[1] <= TILESIZE//2 and event_sprite.hitbox.bottomleft[0] <= player.hitbox.center[0] <= event_sprite.hitbox.bottomright[0]
        elif "left" in player.status:
            trigger = -TILESIZE//2 <= player.hitbox.topleft[0] - event_sprite.hitbox.topright[0] <= TILESIZE//2 and event_sprite.hitbox.topright[1] <= player.hitbox.center[1] <= event_sprite.hitbox.bottomright[1]
        elif "right" in player.status:
            trigger = -TILESIZE//2 <= event_sprite.hitbox.topleft[0] - player.hitbox.topright[0] <= TILESIZE//2 and event_sprite.hitbox.topleft[1] <= player.hitbox.center[1] <= event_sprite.hitbox.bottomleft[1]
        return trigger

    def button_event_listener(self, event_sprite):
        keys = pygame.key.get_pressed()

        if not self.mapctrl.level.player.is_keyboard_forbidden:
            if (keys[pygame.K_z] or keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
                if self.is_event_listening:
                    return self.event_sprite_collision_judge(event_sprite)
        return False

    def touch_event_listener(self, event_sprite):
        if not self.mapctrl.level.player.is_keyboard_forbidden:
            if self.is_event_listening:
                return self.event_sprite_collision_judge(event_sprite)
        return False

    def switch_event_listening(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_z] or keys[pygame.K_SPACE] or keys[pygame.K_RETURN]):
            if self.is_event_listening:
                self.is_event_listening = False
        else:
            self.is_event_listening = True

    def run(self):
        lock_player = False
        for commonevent in self.commonevents:
            commonevent.run()
            lock_player = lock_player or commonevent.lock_player
        for commonevent in self.bg_commonevents:
            commonevent.run()
            lock_player = lock_player or commonevent.lock_player
        if lock_player:
            self.mapctrl.level.lock_player()
        else:
            self.mapctrl.level.unlock_player()

        self.switch_event_listening()

