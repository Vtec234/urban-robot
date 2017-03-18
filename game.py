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
        self._WIDTH = 256
        self._HEIGHT = 256
        self._PLAYERX = self._WIDTH/2
        self._PLAYERY = self._HEIGHT/2
        self._MONSTERS = []

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
