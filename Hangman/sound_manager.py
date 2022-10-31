import pygame
from pygame import mixer
class Sound_manager():
    def __init__(self,sound_path,chanel,volume,offset_event) -> None:
        mixer.init()
        self.sound = mixer.Sound(sound_path)
        self.channel = chanel
        self.sound.set_volume(volume)
        self.is_stop_sound = False
        self.offset_event = offset_event
        mixer.Channel(self.channel).set_endevent(pygame.USEREVENT+offset_event)
    def play_sound(self):
        self.is_stop_sound = False
        mixer.Channel(self.channel).play(self.sound)
    def stop_sound(self):
        self.is_stop_sound = True
        mixer.Channel(self.channel).stop()