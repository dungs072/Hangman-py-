import pygame
class Animation():
    def __init__(self,images:list,x,y) -> None:
        self.images = images
        self.x = x
        self.y = y
        self.count = -1
        
    def draw(self,WIN):
        self.count = (self.count+1)%len(self.images)
        WIN.blit(self.images[self.count],(self.x,self.y)) 
        pygame.time.delay(100)