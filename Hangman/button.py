import pygame
from pygame import mixer
pygame.font.init()
class Button():
    def __init__(self, x,y,image,scale,title = '',size_text = 30,infor = None,count_click = -1,clicked_image = None,song_path = None,wait_time_trigger_event = 0,chanel = 1,need_time_reset = True) -> None:
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
        self.clicked_image = clicked_image
        self.need_time_reset = need_time_reset
        if clicked_image!=None:
            self.clicked_image = pygame.transform.scale(clicked_image,(int(width*scale),int(height*scale)))
        self.time_since_unclicked = 0
        self.time_per_unclicked = 300
        self.time_since_unclicked2 = 0
        self.time_per_unclicked2 = 700
        self.time_since_last_trigger_event = 0
        self.wait_time_trigger_event = wait_time_trigger_event
        self.current_image = self.image if clicked_image ==None else clicked_image
        self.sound = None
        self.channel = chanel
        if song_path!=None:
            mixer.init()
            self.sound = mixer.Sound(song_path)
    def draw(self,WIN):
        if self.clicked and self.wait_time_trigger_event>0:
            if pygame.time.get_ticks()-self.time_since_last_trigger_event>=self.wait_time_trigger_event:
                if self.clicked:
                    self.Trigger_event()
                    self.clicked = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1: # 0 = left click, 1 = right click
                if self.clicked_image!=None:
                    self.current_image = self.clicked_image
                    self.time_since_unclicked = pygame.time.get_ticks()
                    self.time_since_unclicked2 = pygame.time.get_ticks()
                    self.time_since_last_trigger_event = pygame.time.get_ticks()
                if self.clicked ==False:
                    self.clicked = True
                    if self.sound!=None and self.can_click==True:
                        self.play_sound()
                    if self.event_trigger!=None and self.can_click==True and self.wait_time_trigger_event==0: 
                        self.Trigger_event()
        if pygame.mouse.get_pressed()[0] ==0: # left mouse is not pressed
                if pygame.time.get_ticks()-self.time_since_unclicked>=self.time_per_unclicked:
                    self.current_image = self.image   
                if pygame.time.get_ticks()-self.time_since_unclicked2>=self.time_per_unclicked2 or self.clicked_image==None:
                    self.clicked = False  
                    
        #draw button on screen
        WIN.blit(self.current_image,(self.rect.x,self.rect.y))
        if(self.title==''): return
        textTBD = self.text_font.render(self.title,1,(0,0,0))
        posX = self.rect.x+int(self.current_image.get_width()/2)-int(textTBD.get_width()/2)
        posY = self.rect.y +int(self.current_image.get_height()/2)-int(textTBD.get_height()/2)
        
        WIN.blit(textTBD,(posX,posY))

    def Trigger_event(self):
        if self.need_argu:
            self.event_trigger(self.infor, self.rect.x,self.rect.y)
        else:
            self.event_trigger()
        if self.count_click !=-1:
            self.can_click = False
        
    def subscribe(self,on_done,need_argu = True):
        self.need_argu = need_argu
        self.event_trigger = on_done
   
    def get_text(self):
        return self.textTBD
    def set_can_click(self,can_click):
        self.can_click = can_click
    def get_clicked(self):
        return self.clicked
    def get_position(self):
        return (self.rect.x,self.rect.y)
    def get_bottom_right_pos(self):
        return self.rect.bottomright
    def play_sound(self):
        mixer.Channel(self.channel).play(self.sound)
    def stop_sound(self):
        mixer.Channel(self.channel).stop(self.sound)