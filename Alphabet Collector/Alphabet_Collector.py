godmode = False
import pygame
import random
from pygame.locals import *
import time
pygame.init()
clock = pygame.time.Clock()
clock.tick(60)
screen = pygame.display.set_mode((500,600))

hearts = pygame.image.load("hearts.png").convert_alpha()

myfont = pygame.font.SysFont("impact", 40)
bigfont = pygame.font.SysFont("impact", 70)
startfont = pygame.font.SysFont("impact", 50)
start_mess = startfont.render("Alphabet Collector", True, (255,255,255))
start_rect = start_mess.get_rect(center=(250,150))
start_button = pygame.Rect(200,450,100,50)
start_mess2 = myfont.render("Start", True, (255,255,255))
start_rect2 = start_mess2.get_rect(center=(250,475))

gameover_mess = bigfont.render("GAMEOVER", True, (255,0,0))
gameover_rect = gameover_mess.get_rect(center=(250,200))
gameover_mess2 = myfont.render("Press any key to continue.", True, (255,0,0))
gameover_rect2 = gameover_mess2.get_rect(center=(250,450))

pause_mess = bigfont.render("PAUSED", True, (255,0,0))
pause_rect = pause_mess.get_rect(center=(250,300))

paused = False
gameover = False
def drawplayer():
    pygame.draw.rect(screen, (250,250,250), player)
def updatefood():
    global food
    global lives
    for i in food:
        i['y'] += foodspeed
        f_rect = pygame.Rect(i['x'], i['y'], 50,50)
        mark = chr(i['mark'])
        markblit = myfont.render(mark, True, (0,0,0))
        m_rect = markblit.get_rect(center=(i['x']+25, i['y']+25))
        pygame.draw.rect(screen, (0,255,0), f_rect)
        screen.blit(markblit, m_rect)
        if i['y'] > 600:
            if 65 <= i['mark'] <= 90:
                lives -= 1
            food.remove(i)
            
def checkcollide():
    global score
    global lives
    for item in food:
        f_rect = pygame.Rect(item['x'], item['y'], 50,50)
        if player.colliderect(f_rect):
            food.remove(item)
            if 65 <= item['mark'] <= 90:
                score += 1
            else:
                lives -= 1
def pause():
    global paused
    pausescreen = screen.copy()
    while paused:
        screen.blit(pausescreen, (0,0))
        screen.blit(pause_mess, pause_rect)
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p:
                    paused = False
            elif ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.flip()
def showscore():
    scoremess = myfont.render(("Score: "+str(score)), True, (255,250,250))
    screen.blit(scoremess, (10,10))
    for i in range(lives):
        screen.blit(hearts, (i*60 + 310, 10))

def checkboost():
    global boostbar
    global movespeed
    if boost == True:
        if boostbar > 0:
            movespeed = 15
            boostbar -= 1
        else:
            movespeed = 5
    else:
        movespeed = 5
        if gamecount%10 == 0:
            if boostbar < 100:
                boostbar += 1
    boostrect = pygame.Rect(20,150,50,200)
    currentboost = pygame.Rect(20,(100-boostbar*2)+250, 50, boostbar*2)
    pygame.draw.rect(screen, (150,20,100), currentboost)
    pygame.draw.rect(screen, (0,0,0), boostrect, 4)

gameloop = True
gamecount = 0
state = 'menu'
while gameloop:
    if state == 'game':
        clock.tick(60)
        gamecount += 1
        screen.fill((0,0,255))
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_a or ev.key == pygame.K_LEFT:
                    movex = -1
                elif ev.key == pygame.K_d or ev.key == pygame.K_RIGHT:
                    movex = 1
                elif ev.key == pygame.K_p:
                    paused = True
                elif ev.key == pygame.K_SPACE:
                    boost = True
                pygame.event.clear()
            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_SPACE:
                    boost = False
                elif ev.key == pygame.K_a or ev.key == pygame.K_LEFT:
                    movex += 1
                elif ev.key == pygame.K_d or ev.key == pygame.K_RIGHT:
                    movex -= 1
            elif ev.type == pygame.QUIT:
                pygame.quit()
                quit()
        if movex > 1:
            movex = 1
        elif movex < -1:
            movex = -1
        if -1 < player.x + movex*movespeed < 426:
            player.x += movex*movespeed
        if gamecount%foodspawn == 0:
            mark = random.randint(1,4)
            if mark == 1:
                newfood = {'x':random.randint(0,450), 'y':0, 'mark':random.randint(49,57)}
            else:
                newfood = {'x':random.randint(0,450), 'y':0, 'mark':random.randint(65,90)}
                if chr(newfood['mark']) == 'O':
                    newfood = {'x':random.randint(0,450), 'y':0, 'mark':65}
            food.append(newfood)
        if gamecount%300 == 0:
            foodspeed += 0.2
            if foodspawn > 2:
                foodspawn -= 2
        if score%50 == 0 and lives < 3:
            lives += 1
        drawplayer()
        updatefood()
        checkboost()
        checkcollide()
        showscore()
        pygame.display.flip()
        if lives == 0 and godmode == False:
            #gameoverscreen = screen.copy()
            #screen.blit(gameoverscreen, (0,0))
            screen.blit(gameover_mess, gameover_rect)
            screen.blit(gameover_mess2, gameover_rect2)
            pygame.display.flip()
            time.sleep(2)
            pygame.event.clear()
            gameover = True
            while gameover:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif ev.type == pygame.KEYDOWN:
                        gameover = False
                        state = 'menu'
        if paused:
            pause()
    elif state == 'menu':
        screen.fill((0,0,255))
        screen.blit(start_mess, start_rect)
        pygame.draw.rect(screen, (10,190,10), start_button)
        screen.blit(start_mess2, start_rect2)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = ev.pos
                if start_button.collidepoint(pos):
                    score = 0
                    movex = 0
                    movespeed = 5
                    lives = 3
                    boostbar = 100
                    boost = False
                    food = []
                    foodspeed = 3
                    foodspawn = 60
                    player = pygame.Rect(225,525,75,75)
                    state = 'game'
                    pygame.event.clear()
        pygame.display.flip()
