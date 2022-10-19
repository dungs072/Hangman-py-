import pygame
class Button():
    def __init__(self, x,y,image,scale,infor = None) -> None:
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.infor = infor
        self.event_trigger = None
    def draw(self,WIN):
        
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked ==False: # 0 = left click, 1 = right click
                self.clicked = True
                if self.event_trigger!=None: self.event_trigger(self.infor)
        if pygame.mouse.get_pressed()[0] ==0: # left mouse is not pressed
            self.clicked = False
        #draw button on screen
        WIN.blit(self.image,(self.rect.x,self.rect.y))
        
    def subscribe(self,on_done):
        self.event_trigger = on_done
   