import pygame
from my_text import My_Text
from button import Button
class Menu():
    def __init__(self,x,y,scale,background_image) -> None:
        self.x = x
        self.y = y
        width = background_image.get_width()
        height = background_image.get_height()
        self.background = pygame.transform.scale(background_image,(int(width*scale),int(height*scale)))
        self.rect = self.background.get_rect()
        self.rect.topleft = (x,y)
        self.texts = []
        self.buttons =[]
        
    def create_text(self,title,x,y,scale,background_image):
        x = x+self.rect.x
        y = y+self.rect.y
        self.texts.append(My_Text(title,x,y,scale,background_image= background_image))
    def create_button(self,image,x,y,scale,title = '',size_text = 30,clicked_image = None):
        x = x+self.rect.x
        y = y+self.rect.y
        self.buttons.append(Button(x,y,image,scale,title,size_text,clicked_image=clicked_image))
        return self.buttons[-1]
    
    def draw(self,WIN):
        WIN.blit(self.background,(self.rect.x,self.rect.y))
        for button in self.buttons:
            button.draw(WIN)
        for text in self.texts:
            text.draw(WIN)
         
    