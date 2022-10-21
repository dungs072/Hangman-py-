import pygame

class Animation():
    def __init__(self,images:list,x,y,time_per_image) -> None:
        self.images = images
        self.x = x
        self.y = y
        self.count = -1
        self.start_time = 0
        self.time_per_image = time_per_image
    
        
    def draw(self,WIN):
        if pygame.time.get_ticks()-self.start_time<self.time_per_image:
            WIN.blit(self.images[self.count],(self.x,self.y)) 
        else:
            self.start_time = pygame.time.get_ticks()
            self.count = (self.count+1)%len(self.images)
            WIN.blit(self.images[self.count],(self.x,self.y)) 
        