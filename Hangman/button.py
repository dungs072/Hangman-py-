import pygame
pygame.font.init()
class Button():
    def __init__(self, x,y,image,scale,title = '',size_text = 30,infor = None,count_click = -1) -> None:
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.infor = infor
        self.event_trigger = None
        self.text_font = pygame.font.SysFont('monospace',size_text)
        self.title = title
        self.need_argu = True
        self.can_click = True
        self.count_click = count_click
    def draw(self,WIN):
      
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked ==False: # 0 = left click, 1 = right click
                self.clicked = True
                if self.event_trigger!=None and self.can_click==True: 
                    if self.need_argu:
                        self.event_trigger(self.infor, self.rect.x,self.rect.y)
                    else:
                        self.event_trigger()
                    if self.count_click !=-1:
                        self.can_click = False
        if pygame.mouse.get_pressed()[0] ==0: # left mouse is not pressed
            self.clicked = False
        #draw button on screen
        WIN.blit(self.image,(self.rect.x,self.rect.y))
        if(self.title==''): return
        textTBD = self.text_font.render(self.title,1,(0,0,0))
        posX = self.rect.x+int(self.image.get_width()/2)-int(textTBD.get_width()/2)
        posY = self.rect.y +int(self.image.get_height()/2)-int(textTBD.get_height()/2)
        
        WIN.blit(textTBD,(posX,posY))
        
    def subscribe(self,on_done,need_argu = True):
        self.need_argu = need_argu
        self.event_trigger = on_done
   
    def get_text(self):
        return self.textTBD
    def set_can_click(self,can_click):
        self.can_click = can_click