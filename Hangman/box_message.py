import pygame
from button import Button
from my_text import My_Text
class Box_message():
    def __init__(self,image,x,y,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.buttons = []
        self.texts = []
        
    def draw(self,WIN):
        WIN.blit(self.image,(self.rect.x,self.rect.y))
        if len(self.buttons)>0:
            for button in self.buttons:
                button.draw(WIN)
        if len(self.texts)>0:
            for text in self.texts:
                text.draw(WIN)
        
    def create_button(self,image,x,y,scale,title = '',size_text = 30):
        x = x+self.rect.x
        y = y+self.rect.y
        self.buttons.append(Button(x,y,image,scale,title,size_text))
        return self.buttons[-1]
    def create_text(self,title,x,y,scale,background_image,image_text=None):
        x = x+self.rect.x
        y = y+self.rect.y
        self.texts.append(My_Text(title,x,y,scale,background_image))