
import pygame
from pygame import mixer
from button import Button
from my_text import My_Text
class Box_message():
    def __init__(self,image,x,y,scale,sound_path = None,y_scale = 1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale*y_scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.buttons = []
        self.texts = []
        self.sound = None
        if sound_path!=None:
            mixer.init()
            self.sound = mixer.Sound(sound_path)
       
            
                        
    def draw(self,WIN):
        WIN.blit(self.image,(self.rect.x,self.rect.y))
        if len(self.buttons)>0:
            for button in self.buttons:
                button.draw(WIN)
        if len(self.texts)>0:
            for text in self.texts:
                text.draw(WIN)
        
    def create_button(self,image,x,y,scale,title = '',size_text = 30,clicked_image = None,sound_path = '',time_trigger_event = 0,channel = 1,):
        x = x+self.rect.x
        y = y+self.rect.y
        self.buttons.append(Button(x,y,image,scale,title,size_text,clicked_image=clicked_image,song_path=sound_path,wait_time_trigger_event=time_trigger_event,chanel=channel))
        return self.buttons[-1]
    def create_text(self,title,x,y,scale,background_image = None,image_text=None,size_text = 30):
        x = x+self.rect.x
        y = y+self.rect.y
        self.texts.append(My_Text(title,x,y,scale,background_image= background_image,size_font=size_text))
        return self.texts[-1]
    def play_sound(self):
        mixer.Channel(1).play(self.sound)
        
    def stop_sound(self):
        mixer.Channel(1).stop()