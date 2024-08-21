import pygame

class BGM(pygame.mixer.Sound):
    all_sounds: list[pygame.mixer.Sound] = []
    current_volume = 1.0

    def __init__(self, filepath):
        super().__init__(filepath)
        self.set_volume(BGM.current_volume)
        self.__class__.all_sounds.append(self)

    @classmethod
    def set_global_volume(cls, volume):
        cls.current_volume = volume
        for sound in cls.all_sounds:
            sound.set_volume(volume)

    @classmethod
    def remove_sound(cls, sound):
        cls.all_sounds.remove(sound)
    
    @classmethod
    def stop_all(cls):
        for sound in cls.all_sounds:
            sound.stop()

class BGS(pygame.mixer.Sound):
    all_sounds: list[pygame.mixer.Sound] = []
    current_volume = 1.0

    def __init__(self, filepath):
        super().__init__(filepath)
        self.set_volume(BGS.current_volume)
        self.__class__.all_sounds.append(self)

    @classmethod
    def set_global_volume(cls, volume):
        cls.current_volume = volume
        for sound in cls.all_sounds:
            sound.set_volume(volume)

    @classmethod
    def remove_sound(cls, sound):
        cls.all_sounds.remove(sound)
    
    @classmethod
    def stop_all(cls):
        for sound in cls.all_sounds:
            sound.stop()

class SE(pygame.mixer.Sound):
    all_sounds: list[pygame.mixer.Sound] = []
    current_volume = 1.0

    def __init__(self, filepath):
        super().__init__(filepath)
        self.set_volume(SE.current_volume)
        self.__class__.all_sounds.append(self)

    @classmethod
    def set_global_volume(cls, volume):
        cls.current_volume = volume
        for sound in cls.all_sounds:
            sound.set_volume(volume)

    @classmethod
    def remove_sound(cls, sound):
        cls.all_sounds.remove(sound)
    
    @classmethod
    def stop_all(cls):
        for sound in cls.all_sounds:
            sound.stop()

switch_sound = SE("../Audio/SE/yisell_sound.ogg")
choose_sound = SE("../Audio/SE/choose_sound.ogg")

