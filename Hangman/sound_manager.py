import pygame
from pygame import mixer
class Sound_manager():
    def __init__(self,sound_path,chanel,volume) -> None:
        mixer.init()
        self.sound = mixer.Sound(sound_path)
        self.channel = chanel
        self.sound.set_volume(volume)
    def play_sound(self):
        mixer.Channel(self.channel).play(self.sound)
    def stop_sound(self):
        mixer.Channel(self.channel).stop(self.sound)

    