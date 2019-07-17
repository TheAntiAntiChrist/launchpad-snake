from launchpad_py import *
import pygame
from random import randint

pygame.init()
screen = pygame.display.set_mode([50,50])

#63 is max colour value for setting launchpad rbg values (mk2)
lp = LaunchpadMk2()

lp.Open( 0, "mk2" )

lp.ButtonFlush()

x = 0
y = 1
xDirRight = True
Done = False
clock = pygame.time.Clock()

snk = [[0,8]]
snkDir = 0 # 0 is north, 1 is east, 2 is south, 3 is west
counter = 0
length = 1
isEaten = True
alreadyPressed = False

def OOB():
    if snk[-1][0] < 0:
        return True
    elif snk[-1][0] >= 9:
        return True
    if snk[-1][1] < 0:
        return True
    elif snk[-1][1] >= 9:
        return True

while not Done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Done = True
            if event.key == pygame.K_UP and snkDir != 2 and alreadyPressed == False:
                snkDir = 0
                alreadyPressed = True
            if event.key == pygame.K_DOWN and snkDir != 0 and alreadyPressed == False:
                snkDir = 2
                alreadyPressed = True
            if event.key == pygame.K_RIGHT and snkDir != 3 and alreadyPressed == False:
                snkDir = 1
                alreadyPressed = True
            if event.key == pygame.K_LEFT and snkDir != 1 and alreadyPressed == False:
                snkDir = 3
                alreadyPressed = True
    lp.ButtonFlush()
    lp.LedAllOn(0)

    if isEaten:
        ticTac = [randint(1,7), randint(1,7)]
        isEaten = False
    lp.LedCtrlXY(ticTac[0],ticTac[1], 63,0,0)

    if snkDir == 0:
        snk.append([snk[-1][0],snk[-1][1]-1])
    elif snkDir == 1:
        snk.append([snk[-1][0]+1,snk[-1][1]]) #0+10
    elif snkDir == 2:
        snk.append([snk[-1][0],snk[-1][1]+1]) #1+10
    elif snkDir == 3:
        snk.append([snk[-1][0]-1,snk[-1][1]]) #0-10
    if snk[-1] == ticTac:
        length += 1
        #pointSound.play() #Code only useful if ticTac.ogg is present
        isEaten = True
    if len(snk) > length:
        snk.pop(0)
    if OOB():
        print("""
        You Died...
        """)
        print("""
        You Scored: """, length-1, """ points.
        """)
        Done = True
    for segment in snk:
        lp.LedCtrlXY(segment[0],segment[1],0,63,0)
        if snk[-1] == segment and segment is not snk[-1]: #snk[-1] == segment checks value, segment is not snk[-1] shows that the current segment isn't the actual snk[-1]
            print("""
            You Died...
            """)
            print("""
            You Scored: """, length-1, """ points.
            """)
            Done = True


    alreadyPressed = False
    clock.tick(8)

lp.LedAllOn(0)
lp.ButtonFlush()
lp.Close()
