import pygame

class Animation():
    def __init__(self,images:list,x,y,time_per_image,image_draw_at_one_time = None) -> None:
        self.images = images
        self.x = x
        self.y = y
        self.count = -1
        self.start_time = 0
        self.time_per_image = time_per_image
        self.image_draw_at_one_time = image_draw_at_one_time
        
    def draw(self,WIN,can_loop = True):
        if pygame.time.get_ticks()-self.start_time<self.time_per_image:
            WIN.blit(self.images[self.count],(self.x,self.y)) 
        else:
            self.start_time = pygame.time.get_ticks()
            if can_loop:
                self.count = (self.count+1)%len(self.images)
            else:
                self.count = min(self.count+1,len(self.images)-1)
            WIN.blit(self.images[self.count],(self.x,self.y)) 
            
    def set_position(self,x,y):
        self.x = x
        self.y = y
    
    def draw_perplex(self,WIN):
        if pygame.time.get_ticks()-self.start_time<self.time_per_image:
            WIN.blit(self.images[self.count],(self.x,self.y))  
        
        
        