import pygame
import os
import button
import quizz_manager
WIDTH, HEIGHT = 900,650
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hang man")

WHITE = (255,255,255)
BLUE = (0,0,255)

FPS = 60

BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets\\Hangman','Background.jpg'))
PILE_IMAGE = pygame.image.load(os.path.join('Assets\\Hangman','Pile.png'))
BACKGROUND_TEXT_IMAGE = pygame.image.load(os.path.join('Assets\\Text','ImageText.png'))
PILE = pygame.transform.scale(PILE_IMAGE,(600,300))
BACKGROUND_TEXT = pygame.transform.scale(BACKGROUND_TEXT_IMAGE,(200,50))
#load alpha button image
alpha_images = [pygame.image.load(os.path.join('Assets\\Alphas',chr(x)+'.png')) for x in range(65,91)]

#button class

#load button     
vertical_offset = 0
horizontal_offset = 0 
alpha_button = []
for index, image in enumerate(alpha_images):
    alpha_button.append(button.Button(100+horizontal_offset*75,450+vertical_offset,image,1))
    horizontal_offset+=1
    if(index==9 or index==19): 
        vertical_offset +=60
        horizontal_offset = 0
        if index==19:
            horizontal_offset = 2
        
def draw_window():
    WIN.fill(WHITE)
    
    WIN.blit(BACKGROUND_IMAGE,(0,0))
    WIN.blit(PILE,(100,25))
    WIN.blit(BACKGROUND_TEXT,(350,305))
    for button in alpha_button:
        button.draw(WIN)
    pygame.display.update()
#game loop
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): #catch events
            if event.type ==pygame.QUIT:
                run = False
        quizz_manage = quizz_manager()
        (title,answer) = quizz_manage.get_quiz()
        
        draw_window() 
                
    pygame.quit()
    
if __name__ == "__main__":
    main()