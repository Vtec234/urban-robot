import sys
import pygame
import math
import random
import time


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
        self._POTIONS_LIMIT = 3
        self._MONSTERS_LIMIT = 10
        self._TICK_MS = 1000
        self._ROOM_SIZE = 35
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

    @staticmethod
    def distance(a, b):
        dist = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
        return dist

    # Returns elements of list that fit between minPair and maxPair on both X-axis and Y-axis
    @staticmethod
    def filter(lst, minPair, maxPair):
        newlist = []
        for elem in lst:
            if (elem[0] >= minPair[0]) and (elem[0] <= maxPair[0]):
                if (elem[1] >= minPair[1]) and (elem[1] <= maxPair[1]):
                    newlist.append(elem)
        return newlist

    def convertToLocal(self, globalCoordinates):
        return (globalCoordinates[0]%self._ROOM_SIZE, globalCoordinates[1]%self._ROOM_SIZE, globalCoordinates[0]/self._ROOM_SIZE, globalCoordinates[1]/self._ROOM_SIZE)

    def convertToGlobal(self, localCoordinates):
        return (localCoordinates[2]*self._ROOM_SIZE+localCoordinates[0], localCoordinates[3]*self._ROOM_SIZE+localCoordinates[1])

    def not_too_close(self, pos):
        if self.distance(pos, self._playerPos) < self._mindist:
            return False

        #if too close to goals
        if self.distance(pos, self._pgoal) < self._mindist/2:
            return False

        if self.distance(pos, self._agoal) < self._mindist/2:
            return False

        #if too close to HPs
        for ptn in self._potions:
            if self.distance(ptn, pos) < self._mindist/2:
                return False

        #if too close to monsters
        for mon in self._monsters:
            if self.distance(mon, pos) < self._mindist:
                return False

        return True

        #firstly goals, then hps, then with time being audience introduce hps and monsters
        #new monster, given coordinates
        #cannot be monster in the same place what another monster
        #cannot be too close
    def spawn_monster(self, pos):
        #if too close to player
        if self.not_too_close(pos):
            self._monsters.append(pos)
            return True

        return False

    # new potion
    def spawn_potion(self, pos):
        #if too close to player
        if self.not_too_close(pos):
            self._potions.append(pos)
            return True

        return False

    def add_goals(self):
        # TODO random
        self._pgoal = (20, 20)
        while self.distance(self._pgoal, self._playerPos) > (10 * self._mindist):
            self._pgoal = (20, 20)

        self._agoal = (20, 20)
        while self.distance(self._agoal, self._playerPos) > (10 * self._mindist) or self.distance(self._agoal, self._pgoal) > (5 * self._mindist):
            self._agoal = (20, 20)


    # Runs every game tick (e.g. 1 second)
    def tick(self):
        if self._move == "up" and self._playerPos[1] > 0:
            self._playerPos[1] == self._playerPos[1] - 1
        elif self._move == "down" and self._playerPos[1] < self._HEIGHT:
            self._playerPos[1] == self._playerPos[1] + 1
        elif self._move == "left" and self._playerPos[0] > 0:
            self._playerPos[0] == self._playerPos[0] - 1
        elif self._move == "right" and self._playerPos[0] < self._WIDTH:
            self._playerPos[0] == self._playerPos[0] + 1

    def draw(self):
        size = width, height = 700, 700
        white = (255, 255, 255)
        red = (255, 0, 0)
        black = (0,0,0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        screen = pygame.display.set_mode(size)
        for i in range(0, self._ROOM_SIZE):
            for j in range(0, self._ROOM_SIZE):
                if i==0 or i==self._ROOM_SIZE-1 or j==0 or j==self._ROOM_SIZE-1 :
                    if i==self._ROOM_SIZE/2 or j==self._ROOM_SIZE/2 :
                        pygame.draw.rect(screen, black, [i*20+1, j*20+1, 18, 18])
                    else:
                        pygame.draw.rect(screen, green, [i*20+1, j*20+1, 18, 18])
                else:
                    pygame.draw.rect(screen, white, [i*20+1, j*20+1, 18, 18])
        player = self.convertToLocal(self._playerPos)
        pygame.draw.circle(screen, blue, [(player[0]*size[0]/self._ROOM_SIZE)+(size[0]/self._ROOM_SIZE/2), (player[1]*size[1]/self._ROOM_SIZE)+(size[1]/self._ROOM_SIZE/2)], 4)
        for monster in self.filter(self._monsters, (player[2]*self._ROOM_SIZE, player[3]*self._ROOM_SIZE), (player[2]*self._ROOM_SIZE+self._ROOM_SIZE-1, player[3]*self._ROOM_SIZE+self._ROOM_SIZE-1)):
            monsterLocal = self.convertToLocal(monster)
            pygame.draw.circle(screen, red, [(monsterLocal[0]*size[0]/self._ROOM_SIZE)+(size[0]/self._ROOM_SIZE/2), (monsterLocal[1]*size[1]/self._ROOM_SIZE)+(size[1]/self._ROOM_SIZE/2)], 4)
        
        pygame.display.update()

    # Runs every actual frame (e.g. 1MIL times/sec)
    # Returns whether the update should run again (True) or game shoud be closed (False)
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._move = "up"
                elif event.key == pygame.K_DOWN:
                    self._move = "down"
                elif event.key == pygame.K_LEFT:
                    self._move = "left"
                elif event.key == pygame.K_RIGHT:
                    self._move = "right"

            elif event.type == pygame.QUIT:
                return False

        # This is true every second
        if (int(time.time() * 1000.0)) % self._TICK_MS == 0:
            self.tick()
            self.draw()

        return True

def main():
    pygame.init()
    game = Game()
    game.draw()
    while game.update():
        pass

    pygame.quit()
