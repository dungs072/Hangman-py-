
import math
import pygame
import os
import button
from coin_animation_manager import Coin_Animation_Manager
import my_text
from player import Player
import quizz_manager
import underscore_manager
import box_message
import animation

WIDTH, HEIGHT = 900,650
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hang man")

WHITE = (255,255,255)
BLUE = (0,0,255)

FPS = 60

MAX_CHOICE = 7

DEFAULT_COIN_PER_LEVEL = 10

BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets\\Hangman','Background.jpg'))
PILE_IMAGE = pygame.image.load(os.path.join('Assets\\Hangman','Pile.png'))
BACKGROUND_TEXT_IMAGE = pygame.image.load(os.path.join('Assets\\Text','ImageText.png'))
RIGHT_IMAGE = pygame.image.load(os.path.join('Assets\\Text','Right.png'))
X_IMAGE = pygame.image.load(os.path.join('Assets\\Text','xSign.png'))
PILE = pygame.transform.scale(PILE_IMAGE,(600,300))
BACKGROUND_TEXT = pygame.transform.scale(BACKGROUND_TEXT_IMAGE,(200,50))

#box message
BOX_MESSAGE_IMAGE = pygame.image.load(os.path.join('Assets\\Text','Pop_up.png'))
MY_RECORD_IMAGE = pygame.image.load(os.path.join('Assets\\Text','MyRecord.png'))
#load alpha button image
alpha_images = [pygame.image.load(os.path.join('Assets\\Alphas',chr(x)+'.png')) for x in range(65,91)]
#load man image
man_images = [pygame.image.load(os.path.join('Assets\\Man',str(x)+'.png')) for x in range(1,10)]
#load happy man animation
happy_man_images = [pygame.image.load(os.path.join('Assets\\Animations\\HappyMan','happyman'+str(x)+'.png')) for x in range(1,8)]
#button images
next_button_image = pygame.image.load(os.path.join('Assets\\Button','next_button.png'))
again_button_image = pygame.image.load(os.path.join('Assets\\Button','again_button.png'))
#coin image
coin_image = pygame.image.load(os.path.join('Assets\\Text','Coin.png'))

MANS = [pygame.transform.scale(image,(600,300)) for image in man_images]
HAPPY_MANS = [pygame.transform.scale(image,(600,300)) for image in happy_man_images]
#load backend
quizz_manage = quizz_manager.Quizz_manager()
underscore_manage = underscore_manager.Undercore_manager(15,420,390,alpha_images)
#buttons
alpha_button = []
#load text
title_text = my_text.My_Text('',300,305,1,BACKGROUND_TEXT_IMAGE)   
coin_text = my_text.My_Text('',700,25,0.2,coin_image)
coin_count_text = my_text.My_Text('0',760,25,0.2,width = 50,height=50)
#level
can_next_level = True
is_game_over = False
answer = ''
right_circles = []
x_red = []
CURRENT_MAN = PILE
wrong_answer_count = 0
right_answer_count = 0
#coin animation
#coin_animation = Coin_Animation_Manager(405,400,760,25,15) # you must take values from start point and end point
animation_coins = []
start_time = 0
time_per_coin = 200
count_animation_coin = 0
count_finish_coin = 0
for i in range(0,DEFAULT_COIN_PER_LEVEL):
    animation_coins.append(Coin_Animation_Manager(405,400,760,25,15,50))
#pop up window

next_box = box_message.Box_message(BOX_MESSAGE_IMAGE,0,310,1)
next_box.create_text('',260,25,0.3,MY_RECORD_IMAGE)
happy_man_animation = animation.Animation(HAPPY_MANS,100,25,time_per_image=75)
next_button = next_box.create_button(next_button_image,405,250,1,'',15)


over_box = box_message.Box_message(BOX_MESSAGE_IMAGE,0,305,1)
over_box.create_text('OOPS! YOU DIE',260,25,0.3,BOX_MESSAGE_IMAGE)
again_button = over_box.create_button(again_button_image,405,250,0.1,'',15)


#check is right character in answer
def has_right_character_in_answer(char: str):
    global answer
    return [i for i in range(0,len(answer)) if answer[i]==char]

#next level game
def next_level_game():
    global can_next_level
    global is_game_over
    global right_circles
    global x_red
    global CURRENT_MAN
    global wrong_answer_count
    global right_answer_count
    CURRENT_MAN = PILE
    can_next_level = True
    is_game_over = False
    right_circles = []
    x_red = []
    wrong_answer_count = 0
    right_answer_count = 0
    underscore_manage.delete_old_underscores()
    playerr.add_coin(amount-count_finish_coin)
    
    coin_count_text.set_title(str(playerr.get_coin()))
    for bt in alpha_button:
        bt.set_can_click(True)
    
    create_level()
    for button in alpha_button:
        button.set_can_click(True)
    
#handle game over
def game_over():
    global CURRENT_MAN
    CURRENT_MAN = MANS[MAX_CHOICE+1]
#subscribe event
def on_char_button_clicked(infor,posx,posy):
    global wrong_answer_count
    global CURRENT_MAN
    global right_answer_count
    global can_next_level
    global is_game_over
    global animation_coins
    global amount
    global start_time
    global count_animation_coin
    global count_finish_coin
    right_indexes = has_right_character_in_answer(infor)
    
    if len(right_indexes)>0:
        for i in right_indexes:
            underscore_manage.put_char_onto_underscore(infor,i)
            right_circles.append((posx,posy))
            right_answer_count+=1
        if right_answer_count == len(answer):
            #next_level_game()
            amount = DEFAULT_COIN_PER_LEVEL-wrong_answer_count
            for i in range(0,amount):
                animation_coins[i].reset()
            start_time = pygame.time.get_ticks()
            count_animation_coin = 0
            count_finish_coin = 0
            can_next_level = True
            for button in alpha_button:
                button.set_can_click(False)
    else:
        if(wrong_answer_count>=MAX_CHOICE):
            game_over()
            is_game_over = True
            for button in alpha_button:
                button.set_can_click(False)
            return
        CURRENT_MAN = MANS[wrong_answer_count]
        wrong_answer_count+=1
        x_red.append((posx,posy))

def add_money_to_player():
    global count_finish_coin
    playerr.add_coin(1)
    count_finish_coin+=1
    coin_count_text.set_title(str(playerr.get_coin()))
def draw_X(posx,posy):
    WIN.blit(X_IMAGE,(posx,posy))
def draw_right_circle(posx,posy):
    WIN.blit(RIGHT_IMAGE,(posx,posy))  
def draw_game_play_mechanism():
    WIN.blit(CURRENT_MAN,(100,25))
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
def draw_pass_level():
    next_box.draw(WIN)
    happy_man_animation.draw(WIN)
def draw_game_over():
    over_box.draw(WIN)   
    
def draw_coins():
    global start_time
    global count_animation_coin
    if pygame.time.get_ticks()-start_time<time_per_coin:
        pass
    else:
        start_time = pygame.time.get_ticks()
        count_animation_coin = min(count_animation_coin+1,amount)
    for i in range(0,count_animation_coin):
        animation_coins[i].draw_animation(WIN)
        
def draw_window(): 
    WIN.fill(WHITE)  
    WIN.blit(BACKGROUND_IMAGE,(0,0))
    if can_next_level:
        draw_pass_level()
    elif is_game_over:
        draw_game_play_mechanism()
        draw_game_over()
    else: draw_game_play_mechanism()
    
    coin_text.draw(WIN)
    coin_count_text.draw(WIN)
    if can_next_level:
        # for i in range(0,amount):
        #     animation_coins[i].draw_animation(WIN)
        draw_coins()
    
    pygame.display.update()
    
def start():
    #player
    global playerr
    playerr = Player(0)
    #load button     
    vertical_offset = 0
    horizontal_offset = 0 
    for index, image in enumerate(alpha_images):
        alpha_button.append(button.Button(100+horizontal_offset*75,450+vertical_offset,image,1,infor = chr(index+97),count_click=1))
        horizontal_offset+=1
        if(index==9 or index==19): 
            vertical_offset +=60
            horizontal_offset = 0
            if index==19:
                horizontal_offset = 2
    
    #subscribe event for button
    for bt in alpha_button:
        bt.subscribe(on_char_button_clicked)
    next_button.subscribe(next_level_game,False)
    again_button.subscribe(next_level_game,False)
    #subscribe event for coin animation
    for animation_coin in animation_coins:
        animation_coin.subcribe(add_money_to_player)
    create_level()
def create_level():
    global can_next_level
    global answer
    if(can_next_level == False): return
    (title,answer) = quizz_manage.get_quizz()
    if(title==None and answer==None): return
    print(answer)
    can_next_level = False
    title_text.set_title(title)
    underscore_manage.set_quantity(len(answer))
                
def update():
    pass
   
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