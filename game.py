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

        # Player starts at middle
        self._map[WIDTH/2][HEIGHT/2] = 1

    def update(self):
        pass
        for i in range(:
            self._MONSTERS.
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
        if move == "up" && self._PLAYERY>0
            self._PLAYERY = self._PLAYERY - 1
        elif move == "down" && self._PLAYERY<self._HEIGHT
            self._PLAYERY = self._PLAYERY + 1
        elif move == "left" && self._PLAYERX>0
            self._PLAYERX = self._PLAYERX - 1
        elif move == "right" && self._PLAYERX<self._WIDTH
            self._PLAYERX = self._PLAYERX - 1


        # drawing

    def draw(self):





def main():
    pygame.init()
    game = Gamea()
    if True:
        game.update()
        game.draw()


