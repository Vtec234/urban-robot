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
        self._GRIDSIZE = 35
        self._POTIONS_LIMIT = 3
        self._MONSTERS_LIMIT = 10
        self._playerPos = (self._WIDTH/2, self._HEIGHT/2)
        self._move = ""
        self._monsters = []
        self._potions = []
        self._health = 5
        self._mindist = 4
        self._pgoal = (0, 0)
        self._agoal = (0, 0)

    def get_player_pos(self):
        return self._playerPos

    def get_monsters(self):
        return self._monsters

    def get_potions(self):
        return self._potions

    def get_player_goal(self):
        return self._pgoal

    def get_audience_goal(self):
        return self._agoal

#firstly goals, then hps, then with time being audience introduce hps and monsters

        #new monster, given coordinates  
        #cannot be monster in the same place what another monster
        #cannot be too close  
    def new_mon(self, x, y):
        #if too close to player
        if distance(x,y,PLAYERX,PLAYERY) < _mindist
            return False

        #if too close to goals
        if distance(x,y,_PGX,_PGY) < _mindist/2
            return False

        if distance(x,y,_AGX,_AGY) < _mindist/2
            return False

        #if too close to HPs    
        for h in _HP :
            h1 = _HP[h[0]]
            h2 = _HP[h[1]]
            a = distance(h1,h2,x,y)
            if distance(a,b,x,y) < _mindist/2
                return False

        #if too close to monsters
        for i in _MONSTERS:
            a = _MONSTERS[i[0]]
            b = _MONSTERS[i[1]]
            a = distance(a,b,x,y)
            if distance(a,b,x,y) < _mindist
                return False
        
        _MONSTERS.append((x,y))
        return True

    #new health point
    def new_hp (self, x, y)
        #if too close to player
        if distance(x,y,PLAYERX,PLAYERY) < _mindist
            return False

        #if too close to goals
        if distance(x,y,_PGX,_PGY) < _mindist/2
            return False

        if distance(x,y,_AGX,_AGY) < _mindist/2
            return False

        #if too close to HPs    
        for h in _HP :
            h1 = _HP[h[0]]
            h2 = _HP[h[1]]
            a = distance(h1,h2,x,y)
            if distance(a,b,x,y) < _mindist/2
                return False

        #if too close to monsters
        for i in _MONSTERS:
            a = _MONSTERS[i[0]]
            b = _MONSTERS[i[1]]
            a = distance(a,b,x,y)
            if distance(a,b,x,y) < _mindist
                return False

        _HP.append((x,y))
        return True

    #distance between two points
    def distance(a, b):
        dist = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
        return dist

    def add_goals(self):
        # TODO random
        self._pgoal = (20, 20)
        while distance(self._pgoal, self._playerPos) > (10 * self._MINDIST):
            self._pgoal = (20, 20)

        self._agoal = (20, 20)
        while distance(self._agoal, self._playerPos) > (10 * self._MINDIST) or distance(self._agoal, self._pgoal) > (5 * self._MINDIST):
            self._agoal = (20, 20)

    # Runs every game tick (e.g. 1 second)
    def tick(self):
        if self._MOVE == "up" and self._PLAYERY>0:
            self._PLAYERY = self._PLAYERY - 1
        elif self._MOVE == "down" and self._PLAYERY<self._HEIGHT:
            self._PLAYERY = self._PLAYERY + 1
        elif self._MOVE == "left" and self._PLAYERX>0:
            self._PLAYERX = self._PLAYERX - 1
        elif self._MOVE == "right" and self._PLAYERX<self._WIDTH:
            self._PLAYERX = self._PLAYERX - 1

    def filter(list, maxPair, minPair):
        newlist = []
        for elem in list:
            if (elem[0] >= minPair[0]) and (elem[0] <= maxPair[0]):
                if (elem[1] >= minPair[1]) and (elem[1] <= maxPair[1]):
                    newlist.append(elem)
        return newlist


    def draw(self):
        size = width, height = 700, 700
        white = (255, 255, 255)
        screen = pygame.display.set_mode(size)
        pygame.display.update()
        for i in range(0, self._GRIDSIZE):
            for j in range(0, self._GRIDSIZE):
                pygame.draw.rect(screen, white, [i*20+1, j*20+1, 18, 18])
        pygame.display.update()
        #render graphics to screen

    # Runs every actual frame (e.g. 1MIL times/sec)
    def update(self):
        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP :
                    self._MOVE = "up"
                elif event.key == pygame.K_DOWN :
                    self._MOVE = "down"
                elif event.key == pygame.K_LEFT :
                    self._MOVE = "left"
                elif event.key == pygame.K_RIGHT :
                    self._MOVE = "right"
        # This is true every second
        if (time_milliseconds % 1000) == 0:
            self.tick()
            self.draw()

def main():
    pygame.init()
    game = Game()
    game.draw()
    while True:
        #game.update()
        pygame.event.get()
