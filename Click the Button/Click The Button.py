import pygame
from pygame.locals import *
pygame.init()

import math
import time
import random

clock = pygame.time.Clock()

screen = pygame.display.set_mode((700,500))

button = pygame.Rect(300,200,100,100)


#fonts
myfont = pygame.font.SysFont("impact", 40)
bigfont = pygame.font.SysFont("impact", 50)
texts = ['Click the Button','..','..hmm?', 'Hey, you! Stop that!',
         'Stop clicking me!','Leave me alone!','STOP!!',
         'Oh, I see how it is.','Call me \'The Flash\'','Click me. I dare you.',
         'ENOUGH!!', 'Please stop clicking me. Please.', 'You\'re a bad person.',
         'I hate you.', ]
         
direct = {'x':1, 'y':1}
speed = 0
clickcount = 0
flashmode = False

def movebutton():
    global button
    global direct
    if flashmode:
        button.x = random.randint(0,650)
        button.y = random.randint(0,450)
    else:
        button.x += direct['x']*speed
        button.y += direct['y']*speed
        if not 0 < button.x < 600:
            direct['x'] *= -1
        if not 0 < button.y < 400:
            direct['y'] *= -1
    #pygame.draw.rect(screen, (150,20,20), button)
    pygame.draw.circle(screen, (220,20,20), (button.x+50,button.y+50), 50)

def click():
    global speed
    global direct
    global clickcount
    global flashmode
    clickcount += 1
    if clickcount == 12:
        speed = 0
    elif clickcount == 13:
        speed = 10
    elif clickcount < 6:
        pass
    elif clickcount == 21:
        speed += 10
    elif clickcount == 25:
        speed = 0
    elif clickcount == 27:
        flashmode = True
    elif clickcount == 28:
        flashmode = False
        speed = 0
    elif clickcount > 28:
        pass
    else:
        speed += 2
        direct['x'] *= -1
        direct['y'] *= -1
    print(clickcount)

def printtext():
    if clickcount == 0:
        message = bigfont.render(texts[0], True, (0,0,0))
        mess_rect = message.get_rect(center=(350,100))
    else:
        if clickcount < 6:
            message = myfont.render(texts[clickcount], True, (100,0,0))
        elif clickcount == 12:
            message = myfont.render(texts[6], True, (100,0,0))
        elif clickcount == 21:
            message = myfont.render(texts[7], True, (100,0,0))
        elif clickcount == 25:
            message = myfont.render(texts[8], True, (100,0,0))
        elif clickcount == 26:
            message = myfont.render(texts[9], True, (100,0,0))
        elif clickcount > 27:
            message = myfont.render(texts[clickcount-18], True, (100,0,0))
        else:
            message = myfont.render("", True, (0,0,0))
        mess_rect = message.get_rect(center=(300,150))
    screen.blit(message, mess_rect)


def dramaticpause():
    global clickcount
    printtext()
    pygame.display.flip()
    time.sleep(2)
    pygame.event.clear()
    clickcount += 1

def printscore():
    score = clickcount - 5
    if clickcount > 5:
        if 26 <= clickcount <= 30:
            score -= 1
        score_blit = myfont.render(str(score), True, (0,0,0))
        score_rect = score_blit.get_rect(center=(350,70))
        screen.blit(score_blit, score_rect)
    
gameloop = True
gamecount = 0
while gameloop:
    clock.tick(60)
    gamecount += 1

    screen.fill((255,255,255))
    printtext()
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            pos = ev.pos
            if button.collidepoint(pos):
                if flashmode:
                    flashpick = random.randint(1,1)
                    print('flashpick:', flashpick)
                    if flashpick == 1:
                        click()
                else:
                    click()

    movebutton()
    printscore()

    if clickcount == 21 or clickcount == 25 or clickcount == 28:
        dramaticpause()

    pygame.display.flip()
    
    
