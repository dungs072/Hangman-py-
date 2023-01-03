import pygame
import os
from threading import Thread
from time import sleep
import button
from coin_animation_manager import Coin_Animation_Manager
from UI.menu_game import Menu
import my_text
from player import Player
import quizz_manager
import underscore_manager
import box_message
import animation
import sound_manager

base_font = pygame.font.Font(None,20)
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
#SOUND
CLICKED_SOUND_PATH = 'Assets\\Sounds\\sound_clicked_button.mp3'

BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets\\Hangman','Background.jpg'))
PILE_IMAGE = pygame.image.load(os.path.join('Assets\\Hangman','Pile.png'))
BACKGROUND_TEXT_IMAGE = pygame.image.load(os.path.join('Assets\\Text','ImageText.png'))
RIGHT_IMAGE = pygame.image.load(os.path.join('Assets\\Text','Right.png'))
X_IMAGE = pygame.image.load(os.path.join('Assets\\Text','xSign.png'))
PILE = pygame.transform.scale(PILE_IMAGE,(600,300))
BACKGROUND_TEXT = pygame.transform.scale(BACKGROUND_TEXT_IMAGE,(200,50))

#UI
MENU_IMAGE = pygame.image.load(os.path.join('Assets\\UI','Background_menu.png'))
PAUSE_IMAGE = pygame.image.load(os.path.join('Assets\\UI','Pause_Menu.png'))
PAUSE_BUTTON_CLICKED = pygame.image.load(os.path.join('Assets\\UI','pause_button_clicked.png'))
PAUSE_BUTTON_UNCLICKED = pygame.image.load(os.path.join('Assets\\UI','pause_button_unclicked.png'))
#resize pause_button
PAUSE_CLICKED = pygame.transform.scale(PAUSE_BUTTON_CLICKED,(75,75))
PAUSE_UNCLICKED = pygame.transform.scale(PAUSE_BUTTON_UNCLICKED,(75,75))
BACKGROUND_BUTTON_CLICKED = pygame.image.load(os.path.join('Assets\\UI','Background_button_clicked.png'))
BACKGROUND_EXIT_BUTTON_CLICKED = pygame.image.load(os.path.join('Assets\\UI','Background_button_exit_clicked.png'))
BACKGROUND_BUTTON_UNCLICKED =pygame.image.load(os.path.join('Assets\\UI','Background_button_unclicked.png'))
BACKGROUND_EXIT_BUTTON_UNCLICKED = pygame.image.load(os.path.join('Assets\\UI','Background_exit_unclicked.png'))
HANGMAN_TITLE_IMAGES = [pygame.image.load(os.path.join('Assets\\UI\\Hangman_Title','Hangman_title'+str(x)+'.png')) for x in range(0,4)]
PILE_UI_IMAGES = [pygame.image.load(os.path.join('Assets\\Animations\\Intro','intro'+str(x)+'.png')) for x in range(1,6)]
PILE_UI_IMAGES_BIG = [pygame.transform.scale(image,(500,400)) for image in PILE_UI_IMAGES]
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
#input
user_name_input = ''
#create draw circle/x animation
draw_circle_animations = []
draw_x_animations = []
time_since_last_out_menu = 0
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
# pause
is_pause = False
#high score
is_high_score = False
is_get_high_score = False
#input text
active_input_box = False
#pop up window

next_box = box_message.Box_message(BOX_MESSAGE_IMAGE,0,310,1,'Assets\\Sounds\\success.mp3')
next_box.create_text('',260,25,0.3,background_image= MY_RECORD_IMAGE)
happy_man_animation = animation.Animation(HAPPY_MANS,100,25,time_per_image=100)
cloud_animation1 = animation.Animation(clouds,50,25,time_per_image=500)
cloud_animation2 = animation.Animation(clouds,600,70,time_per_image=500)
next_button = next_box.create_button(next_button_image,415,250,1,'',15,clicked_image=next_clicked_button_image,sound_path=CLICKED_SOUND_PATH,channel=2)
chest_text = next_box.create_text('',330,90,0.5,chest_image)

over_box = box_message.Box_message(BOX_MESSAGE_IMAGE,0,305,1,'Assets\\Sounds\\game_over.mp3')
over_box.create_text('OOPS... YOU FAILED!',260,25,0.3,BOX_MESSAGE_IMAGE)
replay_button = over_box.create_button(replay_button_image,380,150,2,'',15,clicked_image = replay_clicked_button_image,sound_path=CLICKED_SOUND_PATH,channel=2)
#suggest button and text
suggest_button = button.Button(710,120,suggest_button_image,1,'',clicked_image=suggest_clicked_button_image,song_path=CLICKED_SOUND_PATH,chanel=2)
suggest_amount_text = my_text.My_Text('x'+str(COST_SUGGESTION),700,110,0.5,background_image=suggest_times_text_image, size_font=18)
suggest_amount_text.set_y_offset_text(-2)
suggest_coin_text = my_text.My_Text('',747,107,0.1,coin_image)
#check is right character in answer
def has_right_character_in_answer(char: str):
    global answer
    return [i for i in range(0,len(answer)) if answer[i]==char]
#START MENU
is_start_game = False
#reset all buttons
def set_can_click_alpha_buttons():
    sleep(0.2) #second 
    for button in alpha_button:
        button.set_can_click(True)
# create thread
reset_thread = Thread(target = set_can_click_alpha_buttons,args=[])
#replay new level game
def replay_next_level_game():
    print(playerr.coin)
    playerr.coin = 100-(amount-count_finish_coin)
    coin_count_text.set_title(str(playerr.coin))
    next_level_game()
#next level game
def next_level_game():
    global can_next_level
    global is_game_over
    global draw_circle_animations
    global draw_x_animations
    global CURRENT_MAN
    global wrong_answer_count
    global right_answer_count
    global is_pause
    CURRENT_MAN = PILE
    can_next_level = True
    is_game_over = False
    is_pause = False
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

def check_current_score_is_high_score():
    
    for (name,score) in high_score_list:
        if score_amount>score:
            return True
    if len(high_score_list)<11: return True
    return False
#handle game over
def game_over():
    global CURRENT_MAN
    global score_amount
    global is_get_high_score
    CURRENT_MAN = MANS[MAX_CHOICE+1]
    if(score_amount>0 and check_current_score_is_high_score()):
        is_get_high_score = True
        high_score_text.set_title(str(score_amount))
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
        temp_button.play_sound()
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
def draw_game_play():
    
    cloud_animation2.draw(WIN)
    if can_next_level or next_button.get_clicked():
        draw_pass_level()
    elif is_game_over or replay_button.get_clicked():
        draw_game_play_mechanism()
        draw_game_over()
    elif not is_pause:
        draw_game_play_mechanism()
    
    score_text.draw(WIN)
    score_count_text.draw(WIN)
    coin_text.draw(WIN)
    coin_count_text.draw(WIN)
    if can_next_level:
        draw_coins()
    elif is_game_over==False and not is_pause:
        suggest_button.draw(WIN)
        suggest_amount_text.draw(WIN)
        suggest_coin_text.draw(WIN)
    cloud_animation1.draw(WIN)
    
    
    if is_pause:
        pause_menu_ui.draw(WIN)
    else:
        pause_button.draw(WIN)
   
        
def draw_menu_UI():
    main_menu.draw(WIN)
    title_ui.draw(WIN)
    pile_ui.draw(WIN,True)
def draw_input_high_score_UI():
    input_high_score.draw(WIN)
    pygame.draw.rect(WIN,color,input_rect,2)
    text_surface = base_font.render(user_name_input,True,(0,0,0))
    WIN.blit(text_surface,(375,295))
def draw_high_score_ui():
    high_score_title.draw(WIN)
    rank_title.draw(WIN)
    score_title.draw(WIN)
    name_title.draw(WIN)
    back_button.draw(WIN)
    for (text1,text2,text3) in high_score_list_ui:
        text1.draw(WIN)
        text2.draw(WIN)
        text3.draw(WIN)
def draw_window(): 
    WIN.fill(WHITE)  
    WIN.blit(BACKGROUND_IMAGE,(0,0))
    if is_get_high_score:
        draw_input_high_score_UI()
    else:
        if is_high_score:
            draw_high_score_ui()
        else:
            if is_start_game:
                draw_game_play()
            else:
                draw_menu_UI()
    pygame.display.update()
def turn_start_game_on(): 
    global is_start_game
    global is_pause
    is_start_game = True
    is_pause = False
    intro_sound.stop_sound()
    gameplay_sound.play_sound()
    quizz_manage.clear_all_answers()
    replay_game()
def turn_start_game_off():
    global is_start_game
    global is_pause
    global time_since_last_out_menu
    is_start_game = False
    is_pause = False
    time_since_last_out_menu = pygame.time.get_ticks()
    gameplay_sound.stop_sound()
    intro_sound.play_sound()
def exit_game():
    global run
    run = False
def high_score_game():
    global is_high_score
    is_high_score = True
def pause_game():
    global is_pause
    is_pause = True
def unpause_game():
    global is_pause
    is_pause = False
def back_to_menu_game():
    global is_high_score
    is_high_score = False
def replay_game():
    quizz_manage.clear_all_answers()
    playerr.coin = 100
    score_count_text.set_title('0')
    coin_count_text.set_title(str(playerr.coin))
    next_level_game()
def write_high_score_into_file():
   
    highest_score_file = open('top_highest_score.txt','w')
    for (name,score) in high_score_list:
        highest_score_file.write(name +' '+str(score)+'\n')
    highest_score_file.close()
def load_data_into_ui():
    for index, (name,score) in enumerate(high_score_list):
        high_score_list_ui[index][1].set_title(str(score))
        high_score_list_ui[index][2].set_title(str(name))
def read_high_score_onto_file():
    highest_score_file = open('top_highest_score.txt')
    for line in highest_score_file:
        temp = line.split()
        name,score = temp[0], int(temp[1])
        high_score_list.append((name,score))
    highest_score_file.close()
    load_data_into_ui()
def save_high_score():
    global is_get_high_score
    global user_name_input
    is_get_high_score = False
    current_score = int(high_score_text.title)
    if len(user_name_input)==0:
        user_name_input = 'annonymous'
    if len(high_score_list)<11 and len(high_score_list)!=10:
        high_score_list.append((user_name_input,current_score))
    else:
        for index,(name,score) in enumerate(high_score_list):
            if score<=current_score:
                high_score_list.insert(index,(user_name_input,current_score))
                break
    
    
    user_name_input = ''
    if len(high_score_list)>10:
        high_score_list.pop()
    load_data_into_ui()
    write_high_score_into_file()
def start_menu():
    global main_menu
    global pile_ui
    global title_ui
    main_menu = Menu(50,80,0.8,MENU_IMAGE)
    play_button = main_menu.create_button(BACKGROUND_BUTTON_UNCLICKED,30,100,0.8,'PLAY GAME',30,BACKGROUND_BUTTON_CLICKED,500,CLICKED_SOUND_PATH,chanel=2)
    high_score_button = main_menu.create_button(BACKGROUND_BUTTON_UNCLICKED,30,250,0.8,'HIGH SCORES',30,BACKGROUND_BUTTON_CLICKED,500,CLICKED_SOUND_PATH,chanel=2)
    exit_button = main_menu.create_button(BACKGROUND_EXIT_BUTTON_UNCLICKED,30,400,0.8,'EXIT',30,BACKGROUND_EXIT_BUTTON_CLICKED,500,CLICKED_SOUND_PATH,chanel=2)
    title_ui = animation.Animation(HANGMAN_TITLE_IMAGES,170,-10,500)
    pile_ui = animation.Animation(PILE_UI_IMAGES_BIG,500,150,100)
   
    play_button.subscribe(turn_start_game_on,False)#bug
    exit_button.subscribe(exit_game,False)
    high_score_button.subscribe(high_score_game,False)
  
def pause_menu():
    global pause_menu_ui 
    pause_menu_ui = Menu(235,125,0.6,PAUSE_IMAGE,1.5)  
    pause_menu_ui.create_text('PAUSE',190,25,1,None)
    resume_button = pause_menu_ui.create_button(BACKGROUND_BUTTON_UNCLICKED,65,60,0.7,'RESUME',30,BACKGROUND_BUTTON_CLICKED,wait_time_trigger_event=500,sound_path=CLICKED_SOUND_PATH,chanel = 2)    
    play_again_button = pause_menu_ui.create_button(BACKGROUND_BUTTON_UNCLICKED,65,160,0.7,'REPLAY',30,BACKGROUND_BUTTON_CLICKED,wait_time_trigger_event=500,sound_path=CLICKED_SOUND_PATH,chanel = 2)
    exit_menu_button = pause_menu_ui.create_button(BACKGROUND_EXIT_BUTTON_UNCLICKED,65,260,0.7,'BACK MENU',30,BACKGROUND_EXIT_BUTTON_CLICKED,wait_time_trigger_event=500,sound_path=CLICKED_SOUND_PATH,chanel=2)
    
    resume_button.subscribe(unpause_game,False)
    play_again_button.subscribe(replay_game,False)
    exit_menu_button.subscribe(turn_start_game_off,False)
def high_score_ui():
    global high_score_title
    global rank_title
    global score_title
    global name_title
    global back_button
    global high_score_list_ui
    global high_score_list
    high_score_list_ui = []
    high_score_list= []
    high_score_title = my_text.My_Text('HIGH SCORE', 450,72,1)
    rank_title = my_text.My_Text('RANK',223,125,1)
    score_title = my_text.My_Text('SCORE',450,125,1)
    name_title = my_text.My_Text('NAME',673,125,1)
    offset = 40
    for i in range(1,11):
        title1 = ''
        if i == 1:
            title1 = 'st'
        elif i==2:
            title1 = 'nd'
        elif i==3:
            title1 = 'rd'
        else:
            title1 = 'th'
        text1 = my_text.My_Text(str(i)+title1,223,i*offset+125,1)
        text2 = my_text.My_Text('0',450,i*offset+125,1)
        text3 = my_text.My_Text('NONE',673,i*offset+125,1)
        high_score_list_ui.append((text1,text2,text3))
        
    back_button = button.Button(10,550,BACKGROUND_BUTTON_UNCLICKED,0.5,'BACK',30,clicked_image=BACKGROUND_BUTTON_CLICKED,song_path=CLICKED_SOUND_PATH,wait_time_trigger_event=500,chanel = 2)
    back_button.subscribe(back_to_menu_game,False)
    read_high_score_onto_file()
def create_input_high_score_table():
    global input_high_score
    global high_score_text
    global input_rect
    global color
    input_high_score = box_message.Box_message(PAUSE_IMAGE,275,150,0.4,sound_path=CLICKED_SOUND_PATH,y_scale=2) 
    input_high_score.create_text('CONGRATULATIONs!',170,15,1,size_text=20)
    input_high_score.create_text('HIGH SCORE: ',110,75,1,size_text=20)
    high_score_text = input_high_score.create_text('',200,75,1,size_text=20)
    input_high_score.create_text('NAME: ',75,150,1,size_text=20)
    input_rect = pygame.Rect(372,285,190,32)
    color = pygame.Color('lightskyblue3')
    save_button = input_high_score.create_button(BACKGROUND_BUTTON_UNCLICKED,80,180,0.5,title = 'SAVE',clicked_image=BACKGROUND_BUTTON_CLICKED,sound_path=CLICKED_SOUND_PATH,time_trigger_event=500,channel=2)
    save_button.subscribe(save_high_score,False)
def start():
    #player
    global playerr
    global intro_sound
    global gameplay_sound
    global pause_button
    start_menu()
    pause_menu()
    high_score_ui()
    create_input_high_score_table()
    playerr = Player(100)
    coin_count_text.set_title(str(playerr.get_coin()))
    score_count_text.set_title(str(score_amount))
    
    intro_sound = sound_manager.Sound_manager('Assets\\Sounds\\menu_intro.mp3',3,0.7,1)
    intro_sound.play_sound()
    gameplay_sound = sound_manager.Sound_manager('Assets\\Sounds\\gameplay_sound.mp3',4,0.4,2)
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
    pause_button = button.Button(5,100,PAUSE_UNCLICKED,1,title = '',clicked_image=PAUSE_CLICKED,song_path=CLICKED_SOUND_PATH,wait_time_trigger_event=500,chanel=2)
    #subscribe event for button
    for bt in alpha_button:
        bt.subscribe(on_char_button_clicked)
    next_button.subscribe(next_level_game,False)
    replay_button.subscribe(replay_next_level_game,False)
    suggest_button.subscribe(substract_money_of_player,False)
    pause_button.subscribe(pause_game,False)
    #subscribe event for coin animation
    for animation_coin in animation_coins:
        animation_coin.subcribe(add_money_to_player)
        
    #thread
    reset_thread.start()
    #create_level()
def create_level():
    global can_next_level
    global answer
    global current_answer
    if(can_next_level == False): return
    (title,answer) = quizz_manage.get_quizz()
    if(title==None and answer==None):
        quizz_manage.clear_all_answers()
        (title,answer) = quizz_manage.get_quizz()
    current_answer = [ 0 for i in range(0,len(answer))]
    print(answer)
    can_next_level = False
    title_text.set_title(title)
    underscore_manage.set_quantity(len(answer))               
#game loop
def main():
    global run
    global user_name_input
    global active_input_box
    clock = pygame.time.Clock()
    run = True
    start()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): #catch events
            if event.type ==pygame.QUIT:
                run = False
            elif event.type == pygame.USEREVENT+intro_sound.offset_event:
                if not intro_sound.is_stop_sound:
                    intro_sound.play_sound()
            elif event.type ==pygame.USEREVENT+gameplay_sound.offset_event:
                if not gameplay_sound.is_stop_sound:
                    gameplay_sound.play_sound()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active_input_box = True
                else:
                    active_input_box = False
            if active_input_box and is_get_high_score and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_name_input = user_name_input[:-1]
                elif event.key ==pygame.K_SPACE:
                    user_name_input = user_name_input
                elif event.key ==pygame.K_RETURN:
                    save_high_score()
                else:
                    if len(user_name_input)<=20:
                        user_name_input+= event.unicode
            
        draw_window() 
                
    pygame.quit()
    
if __name__ == "__main__":
    main()