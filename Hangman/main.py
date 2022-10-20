import pygame
import os
import button
import my_text
import quizz_manager
import underscore_manager

WIDTH, HEIGHT = 900,650
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hang man")

WHITE = (255,255,255)
BLUE = (0,0,255)

FPS = 60

BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets\\Hangman','Background.jpg'))
PILE_IMAGE = pygame.image.load(os.path.join('Assets\\Hangman','Pile.png'))
BACKGROUND_TEXT_IMAGE = pygame.image.load(os.path.join('Assets\\Text','ImageText.png'))
RIGHT_IMAGE = pygame.image.load(os.path.join('Assets\\Text','Right.png'))
X_IMAGE = pygame.image.load(os.path.join('Assets\\Text','xSign.png'))
PILE = pygame.transform.scale(PILE_IMAGE,(600,300))
BACKGROUND_TEXT = pygame.transform.scale(BACKGROUND_TEXT_IMAGE,(200,50))
#load alpha button image
alpha_images = [pygame.image.load(os.path.join('Assets\\Alphas',chr(x)+'.png')) for x in range(65,91)]
#load backend
quizz_manage = quizz_manager.Quizz_manager()
underscore_manage = underscore_manager.Undercore_manager(15,420,390,alpha_images)
#buttons
alpha_button = []
#load text
title_text = my_text.My_Text('',300,305,1,BACKGROUND_TEXT_IMAGE)   
#level
is_next_level = True
answer = ''
right_circles = []
x_red = []
#check is right character in answer
def has_right_character_in_answer(char: str):
    global answer
    return [i for i in range(0,len(answer)) if answer[i]==char]
#subscribe event
def on_char_button_clicked(infor,posx,posy):
    
    right_indexes = has_right_character_in_answer(infor)
    if len(right_indexes)>0:
        for i in right_indexes:
            underscore_manage.put_char_onto_underscore(infor,i)
            right_circles.append((posx,posy))
    else:
        x_red.append((posx,posy))
    
def draw_X(posx,posy):
    WIN.blit(X_IMAGE,(posx,posy))
def draw_right_circle(posx,posy):
    WIN.blit(RIGHT_IMAGE,(posx,posy))  
    
def draw_window(): 
    WIN.fill(WHITE)  
    WIN.blit(BACKGROUND_IMAGE,(0,0))
    WIN.blit(PILE,(100,25))
    
    title_text.draw(WIN)
    for button in alpha_button:
        button.draw(WIN)
    underscore_manage.draw(WIN)
    if(len(right_circles)>0):
        for (posx,posy) in right_circles:
            draw_right_circle(posx,posy)
    if(len(x_red)>0):
        for (posx,posy) in x_red:
            draw_X(posx,posy)
    pygame.display.update()
    
def start():
#load button     
    vertical_offset = 0
    horizontal_offset = 0 
    for index, image in enumerate(alpha_images):
        alpha_button.append(button.Button(100+horizontal_offset*75,450+vertical_offset,image,1,chr(index+97)))
        horizontal_offset+=1
        if(index==9 or index==19): 
            vertical_offset +=60
            horizontal_offset = 0
            if index==19:
                horizontal_offset = 2
      
    #subscribe event
   
    for bt in alpha_button:
        bt.subscribe(on_char_button_clicked)
def create_level():
    global is_next_level
    global answer
    if(is_next_level == False): return
    (title,answer) = quizz_manage.get_quizz()
    if(title==None and answer==None): return
    print(answer)
    is_next_level = False
    title_text.set_title(title)
    underscore_manage.set_quantity(len(answer))
def update():
    create_level()  
#game loop
def main():
    clock = pygame.time.Clock()
    run = True
    start()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): #catch events
            if event.type ==pygame.QUIT:
                run = False
        update()
        
        draw_window() 
                
    pygame.quit()
    
if __name__ == "__main__":
    main()