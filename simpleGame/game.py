## Author: Craig Eckert
## ExDep: PyGame
## simple python food collection game
## use wasd to collect food objects for
## a suprising finish.
## EXIT with ESC or q
import sys, pygame
import random
from time import time
from math import sin, cos
from chars import Player

black = 0, 0, 0
white = 255, 255, 255
orb_speeds = [1, 1]


def initPlayer():
    player = Player("main", "circle.png", 1)
    player.rect.move([170 - 50, 720/2 - 50])
    return player

def initFoods(foodCount):
    foods = []
    for i in range(0, foodCount):
        foods.append(Player("food", "circle_food.png", random.random() + 0.1))
        foods[i].rect = foods[i].rect.move([random.random() * (1280 - 50),
        random.random() * (720 - 50)])
        foods[i].speed = [random.random() * 6 - 3,random.random() * 6 - 3]
    return foods

def eventHandler(events, player, decayFlag):
    for event in events:
        if event.type == pygame.QUIT:           sys.exit()
        elif event.type == pygame.KEYDOWN:
            decayFlag = False
            if event.key == pygame.K_d:
                player.speed = [10,0]
            elif event.key == pygame.K_a:
                player.speed = [-10,0]
            elif event.key == pygame.K_w:
                player.speed = [0,-10]
            elif event.key == pygame.K_s:
                player.speed = [0,10]
            elif event.key == pygame.K_q:       sys.exit()
            elif event.key == pygame.K_ESCAPE:  sys.exit()
        elif event.type == pygame.KEYUP :
            decayFlag = True
    return decayFlag

def moveLogic(decayFlag, object):
    # if object.speed[0] != 0 or object.speed[1] != 0:
    #     player.previousPos.append(player.rect)
    if decayFlag == True:
        if object.speed[0] < 0:
            object.speed[0] = object.speed[0] + 2.0
        elif object.speed[0] > 0:
            object.speed[0] = object.speed[0] - 2.0
        if object.speed[1] < 0:
            object.speed[1] = object.speed[1] + 2.0
        elif object.speed[1] > 0:
            object.speed[1] = object.speed[1] - 2.0

    if object.rect.left < 0 or object.rect.right > pygame.display.get_surface().get_size()[0]:
        object.speed[0] = -object.speed[0]
    if object.rect.top < 0 or object.rect.bottom > pygame.display.get_surface().get_size()[1]:
        object.speed[1] = -object.speed[1]
        
    object.rect = object.rect.move(object.speed)
    return

def bounceLogic(objects, screen):
    for o in objects:
        o.rect = o.rect.move(o.speed)
        if o.rect.left < 0 or o.rect.right > pygame.display.get_surface().get_size()[0]:
            o.speed[0] = -o.speed[0]
        if o.rect.top < 0 or o.rect.bottom > pygame.display.get_surface().get_size()[1]:
            o.speed[1] = -o.speed[1]

def checkCollision(score, player, objects):
    for i in range(0, len(objects)):
        ## check against objs
        try:
            if player.rect.colliderect(objects[i].rect):
                player.scale(score * (objects[i].size[0] * 0.02))
                objects.remove(objects[i])
                score = score + 1
                player.tail += 1

        except:
            break
    return score

def drawScreen(screen, score, player, objects, max_score):
    if score == max_score:
        screen.fill((abs(sin(time()) * 255), abs(cos(time())* 255), 0.7 * 255))
    else:
        screen.fill(black)
    for o in objects:
        screen.blit(o.img, o.rect)
    screen.blit(player.img, player.rect)
    # trying to implement snake component
    # print at every 50th position rect in previousPos
    # for i in range(0, score):
    #     screen.blit(player.img, player.previousPos[50 * i])
    pygame.display.flip()
    pygame.time.wait(1)

## MAIN LOOP
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    score = 0
    max_score = 10
    decayFlag = False

    player = initPlayer()
    foods = initFoods(max_score)

    while(True):
        decayFlag = eventHandler(pygame.event.get(), player, decayFlag)
        moveLogic(decayFlag, player)
        bounceLogic(foods, screen)
        score = checkCollision(score, player, foods)
        drawScreen(screen, score, player, foods, max_score)
