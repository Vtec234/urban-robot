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
        self._PLAYERWIDTH = self._WIDTH/2
        self._PLAYERHEIGHT = self._HEIGHT/2
        # Player starts at middle
        self._map[WIDTH/2][HEIGHT/2] = 1

    def update(self):
        pass
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
        
        
        # drawing

    def draw(self):





def main():
    pygame.init()
    game = Gamea()
    if True:
        game.update()
        game.draw()


