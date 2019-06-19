import pygame
from pygame.locals import *
import random
from time import sleep
pygame.init()
screen = pygame.display.set_mode((500,600))
clock = pygame.time.Clock()
clock.tick(60)
paused = False
myfont = pygame.font.SysFont("impact", 40)
bigfont = pygame.font.SysFont("impact", 70)
startfont = pygame.font.SysFont("impact", 50)

frogF = myfont.render("^", True, (0,255,0))
frogR = myfont.render(">", True, (0,255,0))
frogL = myfont.render("<", True, (0,255,0))
frogD = myfont.render("\/", True, (0,255,0))

frog = pygame.Rect(200, 550, 50,50)
direction = "F"
safe = [{'rect':pygame.Rect(0,450, 500,150), 'move':0}, {'rect':pygame.Rect(0,0,500,50),'move':0}]
alive = True
lograte = 90

def drawfrog():
    pygame.draw.rect(screen, (255,255,255), frog)
    if direction == "F":
        frogrect = frogF.get_rect(center=(frog.x+25, frog.y+25))
        screen.blit(frogF, frogrect)
    elif direction == "R":
        frogrect = frogR.get_rect(center=(frog.x+25, frog.y+25))
        screen.blit(frogR, frogrect)
    elif direction == "L":
        frogrect = frogL.get_rect(center=(frog.x+25, frog.y+25))
        screen.blit(frogL, frogrect)
    else:
        frogrect = frogD.get_rect(center=(frog.x+25, frog.y+25))
        screen.blit(frogD, frogrect)
def updatesafe():
    for zone in safe:
        zone['rect'].x += zone['move']
        if -200 < zone['rect'].x < 500:
            pygame.draw.rect(screen, (0,255,0), zone['rect'])
        else:
            safe.remove(zone)
def updatefrog():
    alive = False
    for zone in safe:
        if frog.colliderect(zone['rect']):
            frog.x += zone['move']
            alive = True
            break
    if alive == False or not -20 < frog.x < 475:
        print("gameover")
        pygame.quit()
        quit()
    if frog.y <= 1:
        win()
def win():
    global gamecount
    global frog
    global direction
    global safe
    global alive
    global lograte
    print("you win")
    frog = pygame.Rect(200, 550, 50,50)
    direction = "F"
    safe = [{'rect':pygame.Rect(0,450, 500,150), 'move':0}, {'rect':pygame.Rect(0,0,500,50),'move':0}]
    alive = True
    gamecount = 0
    lograte += 5
movex = 0
movey = 0
jumpdis = 50
gamecount = 0
gameloop = True
move = False
confirm = False
while gameloop:
    screen.fill((0,0,255))
    clock.tick(60)
    gamecount += 1
    for ev in pygame.event.get():
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_a:
                direction = "L"
            elif ev.key == pygame.K_d:
                direction = "R"
            elif ev.key == pygame.K_s:
                direction = "D"
            elif ev.key == pygame.K_w:
                direction = "F"
            elif ev.key == pygame.K_p:
                paused = True
            elif ev.key == pygame.K_SPACE:
                move = True
        elif ev.type == pygame.KEYUP:
            confirm = True
        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()
    if move and confirm:
        if direction == "L":
            movex = -1
        elif direction == "F":
            movey = -1
        elif direction == "R":
            movex = 1
        else:
            movey = 1
        confirm = False
        move = False
    else:
        movex = 0
        movey = 0
    if -1 < frog.x + movex*jumpdis < 451:
        frog.x += movex*jumpdis
    if -1 < frog.y + movey*jumpdis < 600:
        frog.y += movey*jumpdis
    if gamecount%lograte == 0:
        for i in range(1,4):
            randomy = random.randint(1,8)*50
            if randomy%100 == 0:
                newmove = 1
                newx = -200
            else:
                newmove = -1
                newx = 500
            newzone = {'rect':pygame.Rect(newx,randomy,200,50), 'move':newmove}
            safe.append(newzone)
    updatesafe()
    drawfrog()
    updatefrog()
    pygame.display.flip()
