from math import trunc
import pygame
import os
import random

from my_text import My_Text
class Undercore_manager():
    def __init__(self,number_underscore,x,y,alpha_images) -> None:
        self.underscore_images = [pygame.image.load(os.path.join('Assets\\Underscores','underscore'+str(x)+'.png')) for x in range(0,3)]
        
        self.x = x
        self.y = y
        self.quantity = number_underscore
        self.underscores = []
        self.alpha_images = alpha_images
        
    def __assign_underscore_image(self):
        offset = 60
        xpos = self.x
        if self.quantity%2==0: xpos+=30
        count = trunc(self.quantity/2)*-1
        for i in range(0,self.quantity):
            choice_image = random.choice(self.underscore_images)
            self.underscores.append(My_Text('',xpos+offset*count,self.y,0.4,choice_image))
            count+=1
    def put_char_onto_underscore(self,char,index):
        self.underscores[index].set_text_image(self.alpha_images[ord(str.lower(char))-97])
           
    def set_quantity(self, quantity):
        self.quantity = quantity
        self.__assign_underscore_image()
    def draw(self,WIN):
        if len(self.underscores)==0: return
        for i in range(0,self.quantity):
            self.underscores[i].draw(WIN)
    
    def delete_old_underscores(self):
        self.underscores = []