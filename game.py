import sys
import pygame


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
        self._MOVE = ""
        self._MONSTERS = []
        self._HP = []

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


    def draw(self):
        size = width, height = 400, 400
        white = (255, 255, 255)
        screen = pygame.display.set_mode(size)
        pygame.display.update()
        for i in range(0,10):
            for j in range(0, 10):
                pygame.draw.rect(screen, white, [i*40+2, j*40+2, 36, 36])
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