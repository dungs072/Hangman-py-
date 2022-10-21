import pygame
pygame.font.init()
class My_Text():
    def __init__(self,title,x,y,scale,background_image,image_text=None) -> None:
        self.title = title
        self.text_font = pygame.font.SysFont('monospace',30)
        self.width = int((background_image.get_width()+100)*scale)
        self.height = int(background_image.get_height()*scale)
        self.background_image = pygame.transform.scale(background_image,(self.width,self.height))
        self.x = x
        self.y = y
        self.image_text = image_text
       
    def draw(self,WIN):
        WIN.blit(self.background_image,(self.x,self.y))
        textTBD = self.text_font.render(self.title,1,(0,0,0))
        if(self.image_text==None):
            posX = self.x+int(self.width/2)-int(textTBD.get_width()/2)
            posY = self.y +int(self.height/2)-int(textTBD.get_height()/2)
            WIN.blit(textTBD,(posX,posY))
        else:
            WIN.blit(self.image_text,(self.x+7,self.y-25))
      
    def set_title(self, title):
        self.title = title
    
    def set_pos(self,x,y):
        self.x = x
        self.y = y
    def set_text_image(self,image):
        self.image_text = image