# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 13:43:14 2022

@author: Surendra
"""

#Snake Game Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init()

#worm class
class worm(object):
    introws = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.introws
        i = self.pos[0]
        j = self.pos[1]
        #To draw eyes of snake
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        


#snake class
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = worm(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    #For controlling snake movement
    def move(self):
        global boundaryTouched
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: 
                    c.pos = (c.introws-1, c.pos[1])
                    boundaryTouched = True
                elif c.dirnx == 1 and c.pos[0] >= c.introws-1: 
                    c.pos = (0,c.pos[1])
                    boundaryTouched = True
                elif c.dirny == 1 and c.pos[1] >= c.introws-1: 
                    c.pos = (c.pos[0], 0)
                    boundaryTouched = True
                elif c.dirny == -1 and c.pos[1] <= 0: 
                    c.pos = (c.pos[0],c.introws-1)
                    boundaryTouched = True
                else: 
                    c.move(c.dirnx,c.dirny)
                
                
        
   
    def reset(self, pos):
        self.head = worm(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    #to append the snake length
    def addWorm(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(worm((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(worm((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(worm((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(worm((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

#To create gaiming window
def drawGrid(w, introws, surface):
    sizeBtwn = w // introws
    x = 0
    y = 0
    
    for l in range(introws):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
    pygame.draw.line(surface, (255,0,0), (0,0), (0,w),5)
    pygame.draw.line(surface, (255,0,0), (0,w), (w,w),5)
    pygame.draw.line(surface, (255,0,0), (w,w), (w,0),5)
    pygame.draw.line(surface, (255,0,0), (w,0), (0,0),5)
	
#to update score after each time snake hit the worm      
class scoreboard(object):
    def __init__(self, score = 0, color = (150,150,150)):
        self.score = score
        self.color = color
    def updateScore(self, score):
        self.score = score
    def draw(self, surface):
        font = pygame.font.SysFont(None, 50)
        text = font.render("Score: "+ str(self.score), True, self.color)
        surface.blit(text, (5,5))


#readraw gaming surface when you wanna play again
def redrawWindow(surface):
    global introws, intwidth, s, snack, score
    surface.fill((100,100,10))
    s.draw(surface)
    snack.draw(surface)
    score.draw(surface)
    drawGrid(intwidth,introws, surface)
    pygame.display.update()

#To create initial snake
def randomSnack(introws, item):

    positions = item.body

    while True:
        x = random.randrange(introws)
        y = random.randrange(introws)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)

#To print message when finish the game
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

    
def main():
    #define global variable
    global intwidth, introws, s, snack, score, boundaryTouched
    boundaryTouched = False
    score = scoreboard()
    intwidth = 500
    introws = 20
    win = pygame.display.set_mode((intwidth, intwidth))
    pygame.display.set_caption('Snake game by Surendra')
    #snake color and size
    s = snake((255,0,0), (10,10))
    snack = worm(randomSnack(introws, s), color=(0,255,0))
    flag = True

    clock = pygame.time.Clock()
    #user input to choose the speed of snake
    speed=int(input('Enter speed of the snake [any number BUT number between 5 to 10 is better]:'))
    while flag:
        pygame.time.delay(50)
        clock.tick(speed)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addWorm()
            snack = worm(randomSnack(introws, s), color=(0,255,0))
        score.updateScore(len(s.body)-1)
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])) or boundaryTouched:
                #print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10,10))
                boundaryTouched = False
                break
           
        redrawWindow(win)
    
main()