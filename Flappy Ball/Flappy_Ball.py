import pygame
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
import random
import time

size = (500,600)
screen = pygame.display.set_mode(size)

myfont = pygame.font.SysFont("impact", 40)
titlefont = pygame.font.SysFont("impact", 60)

title = titlefont.render("Flappy Ball", True, (175,0,175))
titlerect = title.get_rect(center=(250,150))

pause_blit = titlefont.render("Paused", True, (255,200,255))
pauserect = pause_blit.get_rect(center=(250,300))
paused = False

start_button = pygame.Rect(200,450,100,50)
start_blit = myfont.render("Start", True, (255,255,255))
startrect = start_blit.get_rect(center=(250,475))

state = 'menu'

def movebird():
    global jump
    global jump_time
    global state
    if bird.y > 550:
        print("gameover\nFinal Score: %i"%score)
        state = 'menu'
    elif not bird.y - 6 <= 1:
        if jump:
            bird.y -= 6
            jump_time -= 1
            if jump_time == 0:
                jump = False
                jump_time = 10
    else:
        jump = False
    if not jump:
        bird.y += 4

def displaybird():
    centerx = bird.x + 25
    centery = bird.y + 25
    pygame.draw.circle(screen, (210,20,210), (centerx,centery), 25)

def displaypipes():
    global pipes
    global score
    global blanks
    global state
    for pipe in pipes:
        pipe['x'] -= 3
        t_rect = pygame.Rect(pipe['x'], 0, 75, pipe['top'])
        b_rect = pygame.Rect(pipe['x'], pipe['bot'], 75, 600)
        pygame.draw.rect(screen, (100,0,100), t_rect)
        pygame.draw.rect(screen, (100,0,100), b_rect)
        rects = [t_rect, b_rect]
        if bird.collidelist(rects) != -1:
            print("gameover\nFinal Score: %i"%score)
            state = 'menu'
    for blank in blanks:
        blank.x -= 3
        if bird.colliderect(blank):
            score += 1
            blanks.remove(blank)
            

def displayscore():
    score_blit = myfont.render(str(score), True, (255,255,255))
    score_rect = score_blit.get_rect(center=(250, 100))
    screen.blit(score_blit, score_rect)

def pause():
    global paused
    pausescreen = screen.copy()
    while paused:
        screen.blit(pausescreen, (0,0))
        screen.blit(pause_blit, pauserect)
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p:
                    paused = False
            elif ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.flip()

    
gameloop = True
gamecount = 0
while gameloop:
    screen.fill((0,0,0))
    if state == 'game':
        clock.tick(60)
        gamecount += 1
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    if not jump:
                        jump = True
                elif ev.key == pygame.K_p:
                    paused = True
        if gamecount%100 == 0:
            valid_pipe = False
            while not valid_pipe:
                middle = random.randint(150,450)
                if abs(middle - lastmid) < 200:
                    break
            lastmid = middle
            newpipe = {'x':500, 'top':middle-75, 'bot':middle+75}
            pipes.append(newpipe)
            blank = pygame.Rect(newpipe['x'], newpipe['top'], 75, newpipe['bot'])
            blanks.append(blank)
        movebird()
        displaybird()
        displaypipes()
        displayscore()
        if paused:
            pause()
    elif state == 'menu':
        screen.blit(title, titlerect)
        pygame.draw.rect(screen,(150,0,150),start_button)
        screen.blit(start_blit, startrect)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = ev.pos
                if start_button.collidepoint(pos):
                    score = 0
                    bird = pygame.Rect(200,200,50,50)
            
                    pipes = []
                    blanks = []
                    lastmid = -1

                    jump = False
                    jump_time = 10
                    
                    state = 'game'
                    pygame.event.clear()

    pygame.display.flip()
    
    
