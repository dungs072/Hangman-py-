import pygame
import os
class Coin_Animation_Manager():
    def __init__(self,startX,startY,desX,desY,xSpeed,time_per_image) -> None:
        self.startX = startX
        self.startY = startY
        self.desX = desX
        self.desY = desY
        self.coin_images = [pygame.image.load(os.path.join('Assets\\Coins','Coin'+str(x)+'.png')) for x in range(1,10)]
        self.xSpeed = xSpeed
        self.current_x_point = startX
        self.current_y_point = startY
        self.current_image = self.coin_images[0]
        self.count = 0
        self.start_time = 0
        self.time_per_image = time_per_image
        self.event_trigger = None
        self.is_in_des = False
    def draw_animation(self,WIN):
        if self.current_x_point > self.desX or self.current_y_point < self.desY:
            if self.is_in_des==False:
                self.event_trigger()
                self.is_in_des = True
            return
        if pygame.time.get_ticks()-self.start_time<self.time_per_image:
            WIN.blit(self.current_image,(self.current_x_point,self.current_y_point))
        else:
            self.start_time = pygame.time.get_ticks()
            self.current_x_point +=self.xSpeed
            self.current_y_point = self.calculate_next_y_point(self.current_x_point)
            self.current_image = self.coin_images[self.count]
            WIN.blit(self.current_image,(self.current_x_point,self.current_y_point))
        
        self.count = (self.count+1)% len(self.coin_images)
        
    
    def calculate_next_y_point(self,xpoint):
        coff1 = (self.startY-self.desY)/(self.startX-self.desX)
        return int(coff1*xpoint + (self.desY-coff1*self.desX))
    
    def reset(self):
        self.current_x_point = self.startX
        self.current_y_point = self.startY
        self.count = 0
        self.start_time = pygame.time.get_ticks()
        self.current_image = self.coin_images[0]
        self.is_in_des = False
    
    def subcribe(self, on_doing):
        self.event_trigger = on_doing