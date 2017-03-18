import sys
import pygame
import math
import random


# World grid type:
# 0 - empty
# 1 - player
# 2 - monster
# 3 - health
# 4 - playerGoal
# 5 - audienceGoal
class Game:
    def __init__(self):
        self._WIDTH = 175
        self._HEIGHT = 175
        self._PLAYERX = self._WIDTH/2
        self._PLAYERY = self._HEIGHT/2
        self._MONSTERS = []
        self._HP = []
        self.numHP = 3
        self.mindist = 4
        self.PGX=0
        self.PGY=0
        self.AGX=0
        self.AGY=0

#firstly goals, then hps, then with time being audience introduce hps and monsters

        #new monster, given coordinates  
        #cannot be monster in the same place what another monster
        #cannot be too close  
    def new_mon(self, x, y):
        #if too close to player
        if distance(x,y,PLAYERX,PLAYERY) < mindist
            return False

        #if too close to goals
        if distance(x,y,PGX,PGY) < mindist/2
            return False

        if distance(x,y,AGX,AGY) < mindist/2
            return False

        #if too close to HPs    
        for h in _HP :
            h1 = _HP[h[0]]
            h2 = _HP[h[1]]
            a = distance(h1,h2,x,y)
            if distance(a,b,x,y) < mindist/2
                return False

        #if too close to monsters
        for i in _MONSTERS:
            a = _MONSTERS[i[0]]
            b = _MONSTERS[i[1]]
            a = distance(a,b,x,y)
            if distance(a,b,x,y) < mindist
                return False
        
        _MONSTERS.append((x,y))
        return True

    #new health point
    def new_hp (self, x, y)
        #if too close to player
        if distance(x,y,PLAYERX,PLAYERY) < mindist
            return False

        #if too close to goals
        if distance(x,y,PGX,PGY) < mindist/2
            return False

        if distance(x,y,AGX,AGY) < mindist/2
            return False

        #if too close to HPs    
        for h in _HP :
            h1 = _HP[h[0]]
            h2 = _HP[h[1]]
            a = distance(h1,h2,x,y)
            if distance(a,b,x,y) < mindist/2
                return False

        #if too close to monsters
        for i in _MONSTERS:
            a = _MONSTERS[i[0]]
            b = _MONSTERS[i[1]]
            a = distance(a,b,x,y)
            if distance(a,b,x,y) < mindist
                return False
        
        _HP.append((x,y))
        return True

    #new player goal
    def new_pg (self, x, y)
        #if too close to player
        if distance(x,y,PLAYERX,PLAYERY) < mindist
            return False

        #if too close to goals
        if distance(x,y,PGX,PGY) < mindist/2
            return False

        if distance(x,y,AGX,AGY) < mindist/2
            return False

        #if too close to HPs    
        for h in _HP :
            h1 = _HP[h[0]]
            h2 = _HP[h[1]]
            a = distance(h1,h2,x,y)
            if distance(a,b,x,y) < mindist/2
                return False

        #if too close to monsters
        for i in _MONSTERS:
            a = _MONSTERS[i[0]]
            b = _MONSTERS[i[1]]
            a = distance(a,b,x,y)
            if distance(a,b,x,y) < mindist
                return False
        
        PGX = x
        PGY = y
        return True


        #new audience goal
    def new_ag (self, x, y)
        #if too close to player
        if distance(x,y,PLAYERX,PLAYERY) < mindist
            return False

        #if too close to goals
        if distance(x,y,PGX,PGY) < mindist/2
            return False

        if distance(x,y,AGX,AGY) < mindist/2
            return False

        #if too close to HPs    
        for h in _HP :
            h1 = _HP[h[0]]
            h2 = _HP[h[1]]
            a = distance(h1,h2,x,y)
            if distance(a,b,x,y) < mindist/2
                return False

        #if too close to monsters
        for i in _MONSTERS:
            a = _MONSTERS[i[0]]
            b = _MONSTERS[i[1]]
            a = distance(a,b,x,y)
            if distance(a,b,x,y) < mindist
                return False
        
        AGX = x
        AGY = y
        return True


    #distance between two points
    def distance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist


    # Runs every game tick (e.g. 1 second)
    def tick(self):
        #for i in range(:
            #self._MONSTERS.

        if move == "up" and self._PLAYERY>0
            self._PLAYERY = self._PLAYERY - 1
        elif move == "down" and self._PLAYERY<self._HEIGHT
            self._PLAYERY = self._PLAYERY + 1
        elif move == "left" and self._PLAYERX>0
            self._PLAYERX = self._PLAYERX - 1
        elif move == "right" and self._PLAYERX<self._WIDTH
            self._PLAYERX = self._PLAYERX - 1

    def draw(self):
        pass
        # render graphics to screen

    # Runs every actual frame (e.g. 1MIL times/sec)
    def update(self);
        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP :
                    move = "up"
                elif event.key == pygame.K_DOWN :
                    move = "down"
                elif event.key == pygame.K_LEFT :
                    move = "left"
                elif event.key == pygame.K_RIGHT :
                    move = "right"

        # This is true every second
        if (time_milliseconds % 1000) == 0:
            self.tick()

        self.draw()

def main():
    pygame.init()
    game = Game()
    if True:
        game.update()
