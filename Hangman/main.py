
from pickle import FALSE
import pygame
import os
from threading import Thread
from time import sleep
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
COST_SUGGESTION = 30

DEFAULT_COIN_PER_LEVEL = 10
DEFAULT_SCORE_PER_LEVEL = 100

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
happy_man_images = [pygame.image.load(os.path.join('Assets\\Animations\\HappyMan','happyman'+str(x)+'.png')) for x in range(1,11)]
#load cloud animation
cloud_images = [pygame.image.load(os.path.join('Assets\\Animations\\Clouds','cloud'+str(x)+'.png')) for x in range(1,6)]
clouds = [pygame.transform.scale(image,(200,100)) for image in cloud_images]
#load draw circle animation
draw_circle_images = [pygame.image.load(os.path.join('Assets\\Animations\\Draw_Circle','circle'+str(x)+'.png')) for x in range(0,6)]
#load draw x animation
draw_x_images = [pygame.image.load(os.path.join('Assets\\Animations\\Draw_X','x'+str(x)+'.png')) for x in range(0,6)]
#button images
next_button_image = pygame.image.load(os.path.join('Assets\\Button\\Next','next.png'))
next_clicked_button_image = pygame.image.load(os.path.join('Assets\\Button\\Next','next_clicked.png'))
replay_button_image = pygame.image.load(os.path.join('Assets\\Button\\Replay','replay.png'))
replay_clicked_button_image = pygame.image.load(os.path.join('Assets\\Button\\Replay','replay_clicked.png'))
suggest_button_image = pygame.image.load(os.path.join('Assets\\Button\\Suggest','suggest.png'))
suggest_clicked_button_image = pygame.image.load(os.path.join('Assets\\Button\\Suggest','suggest_clicked.png'))
#chest image
chest_image = pygame.image.load(os.path.join('Assets\\Items','Chest.png'))
#text images
suggest_times_text_image = pygame.image.load(os.path.join('Assets\\Text','times.png'))
#coin image
coin_image = pygame.image.load(os.path.join('Assets\\Text','Coin.png'))
# text score
score_text = my_text.My_Text('Score: ',50,21,1,size_font=20)
score_count_text = my_text.My_Text('1000',125,21,1,size_font=20)
MANS = [pygame.transform.scale(image,(600,300)) for image in man_images]
HAPPY_MANS = [pygame.transform.scale(image,(600,300)) for image in happy_man_images]
#load backend
quizz_manage = quizz_manager.Quizz_manager()
underscore_manage = underscore_manager.Undercore_manager(15,420,390,alpha_images)
#buttons
alpha_button = []
#load text
title_text = my_text.My_Text('',300,305,1, background_image= BACKGROUND_TEXT_IMAGE)   
coin_text = my_text.My_Text('',700,25,0.2,background_image=coin_image)
coin_count_text = my_text.My_Text('0',760,25,0.2,width = 50,height=50)
answer_text = my_text.My_Text('ANSWER: ',545,233,1)
#create draw circle/x animation
draw_circle_animations = []
draw_x_animations = []
#level
can_next_level = True
is_game_over = False
answer = ''
amount = 0
score_amount = 0
current_answer =[]
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

next_box = box_message.Box_message(BOX_MESSAGE_IMAGE,0,310,1,'Assets\\Sounds\\success.mp3')
next_box.create_text('',260,25,0.3,background_image= MY_RECORD_IMAGE)
happy_man_animation = animation.Animation(HAPPY_MANS,100,25,time_per_image=100)
cloud_animation1 = animation.Animation(clouds,50,25,time_per_image=500)
cloud_animation2 = animation.Animation(clouds,600,70,time_per_image=500)
next_button = next_box.create_button(next_button_image,415,250,1,'',15,clicked_image=next_clicked_button_image)
chest_text = next_box.create_text('',330,90,0.5,chest_image)

over_box = box_message.Box_message(BOX_MESSAGE_IMAGE,0,305,1,'Assets\\Sounds\\game_over.mp3')
over_box.create_text('OOPS... YOU FAILED!',260,25,0.3,BOX_MESSAGE_IMAGE)
replay_button = over_box.create_button(replay_button_image,380,150,2,'',15,clicked_image = replay_clicked_button_image)

#suggest button and text
suggest_button = button.Button(710,120,suggest_button_image,1,'',clicked_image=suggest_clicked_button_image)
suggest_amount_text = my_text.My_Text('x'+str(COST_SUGGESTION),700,110,0.5,background_image=suggest_times_text_image, size_font=18)
suggest_amount_text.set_y_offset_text(-2)
suggest_coin_text = my_text.My_Text('',747,107,0.1,coin_image)
#check is right character in answer
def has_right_character_in_answer(char: str):
    global answer
    return [i for i in range(0,len(answer)) if answer[i]==char]

#reset all buttons
def set_can_click_alpha_buttons():
    sleep(0.2) #second 
    for button in alpha_button:
        button.set_can_click(True)
# create thread
reset_thread = Thread(target = set_can_click_alpha_buttons,args=[])
#next level game
def next_level_game():
    global can_next_level
    global is_game_over
    global draw_circle_animations
    global draw_x_animations
    global x_red_pos
    global CURRENT_MAN
    global wrong_answer_count
    global right_answer_count
    CURRENT_MAN = PILE
    can_next_level = True
    is_game_over = False
    draw_circle_animations.clear()
    draw_x_animations.clear()
    wrong_answer_count = 0
    right_answer_count = 0
    underscore_manage.delete_old_underscores()
    next_box.stop_sound()
    playerr.add_coin(amount-count_finish_coin)
    
    coin_count_text.set_title(str(playerr.get_coin()))
    
    
    create_level()
    #cannot fix this bug right here
    set_can_click_alpha_buttons()
           
#handle game over
def game_over():
    global CURRENT_MAN
    global score_amount
    CURRENT_MAN = MANS[MAX_CHOICE+1]
    score_amount = 0
    score_count_text.set_title(str(score_amount))
    over_box.play_sound()
    answer_text.set_title('Answer: '+answer.upper())

def handle_overcome_challenge():
    global start_time
    global count_animation_coin
    global count_finish_coin
    global can_next_level
    global amount
    global score_amount
    if right_answer_count == len(answer):
        amount = DEFAULT_COIN_PER_LEVEL-wrong_answer_count
        score_amount= score_amount+DEFAULT_SCORE_PER_LEVEL - wrong_answer_count*10
        score_count_text.set_title(str(score_amount))
        for i in range(0,amount):
            animation_coins[i].reset()
        start_time = pygame.time.get_ticks()
        count_animation_coin = 0
        count_finish_coin = 0
        can_next_level = True
        next_box.play_sound()
        answer_text.set_title('Answer: '+answer.upper())
        for button in alpha_button:
            button.set_can_click(False)
            
#subscribe event
def on_char_button_clicked(infor,posx,posy):
    global wrong_answer_count
    global CURRENT_MAN
    global right_answer_count
    global is_game_over
    global animation_coins
    global current_answer
    right_indexes = has_right_character_in_answer(infor)
    
    if len(right_indexes)>0:
        for i in right_indexes:
            underscore_manage.put_char_onto_underscore(infor,i)
            draw_circle_animations.append(animation.Animation(draw_circle_images,posx,posy,50))
            right_answer_count+=1
            current_answer[i] = 1
        handle_overcome_challenge()
    else:
        if(wrong_answer_count>=MAX_CHOICE):
            game_over()
            is_game_over = True
            for button in alpha_button:
                button.set_can_click(False)
            return
        CURRENT_MAN = MANS[wrong_answer_count]
        wrong_answer_count+=1
        draw_x_animations.append(animation.Animation(draw_x_images,posx,posy,50))
    

def find_suggest_index():
    for index,item in enumerate(current_answer):
        if item==0:
            return index 
    return -1
def substract_money_of_player():
    global right_answer_count
    global current_answer
    if playerr.get_coin()>=COST_SUGGESTION:
        playerr.add_coin(-1*COST_SUGGESTION)
        coin_count_text.set_title(str(playerr.get_coin()))
        suggest_index = find_suggest_index()
        right_indexes = has_right_character_in_answer(answer[suggest_index])
        for i in right_indexes:
            underscore_manage.put_char_onto_underscore(answer[i],i)
            right_answer_count+=1
            current_answer[i] = 1
        temp_button = alpha_button[ord(answer[right_indexes[0]])-ord('a')]
        temp_button.set_can_click(False)
        (posx,posy) = temp_button.get_position()
        draw_circle_animations.append(animation.Animation(draw_circle_images,posx,posy,50))
        handle_overcome_challenge()
        
def add_money_to_player():
    global count_finish_coin
    playerr.add_coin(1)
    count_finish_coin+=1
    coin_count_text.set_title(str(playerr.get_coin()))
def draw_game_play_mechanism():
    WIN.blit(CURRENT_MAN,(100,25))
    title_text.draw(WIN)
    for button in alpha_button:
        button.draw(WIN)
    underscore_manage.draw(WIN)
    if(len(draw_circle_animations)>0):
        for animation in draw_circle_animations:
            animation.draw(WIN,False)
    if(len(draw_x_animations)>0):
        for animation in draw_x_animations:
            animation.draw(WIN,False)
def draw_pass_level():
    next_box.draw(WIN)
    answer_text.draw(WIN)
    happy_man_animation.draw(WIN)
def draw_game_over():
    over_box.draw(WIN)   
    answer_text.draw(WIN)
    
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
    cloud_animation2.draw(WIN)
    if can_next_level or next_button.get_clicked():
        draw_pass_level()
    elif is_game_over or replay_button.get_clicked():
        draw_game_play_mechanism()
        draw_game_over()
    else: draw_game_play_mechanism()
    
    score_text.draw(WIN)
    score_count_text.draw(WIN)
    coin_text.draw(WIN)
    coin_count_text.draw(WIN)
    if can_next_level:
        draw_coins()
    elif is_game_over==False:
        suggest_button.draw(WIN)
        suggest_amount_text.draw(WIN)
        suggest_coin_text.draw(WIN)
    cloud_animation1.draw(WIN)
    
    pygame.display.update()
    
def start():
    #player
    global playerr
    playerr = Player(100)
    coin_count_text.set_title(str(playerr.get_coin()))
    score_count_text.set_title(str(score_amount))
    #load button     
    vertical_offset = 0
    horizontal_offset = 0 
    for index, image in enumerate(alpha_images):
        alpha_button.append(button.Button(100+horizontal_offset*75,450+vertical_offset,image,1,infor = chr(index+97),count_click=1,song_path = 'Assets\\Sounds\\write_paper.mp3'))
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
    replay_button.subscribe(next_level_game,False)
    suggest_button.subscribe(substract_money_of_player,False)
    #subscribe event for coin animation
    for animation_coin in animation_coins:
        animation_coin.subcribe(add_money_to_player)
    #thread
    reset_thread.start()
    
    create_level()
def create_level():
    global can_next_level
    global answer
    global current_answer
    if(can_next_level == False): return
    (title,answer) = quizz_manage.get_quizz()
    if(title==None and answer==None): return
    current_answer = [ 0 for i in range(0,len(answer))]
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