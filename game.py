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
        self._map = [[0] * HEIGHT] * WIDTH
        # Player starts at middle
        self._map[WIDTH/2][HEIGHT/2] = 1

    def update(self):
        pass
        # logic
        # drawing

    def draw(self):





def main():
    pygame.init()
    game = Gamea()
    if True:
        game.update()
        game.draw()


