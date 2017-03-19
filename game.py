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
        self._WIDTH = 5*24+1
        self._HEIGHT = 5*24+1
        self._POTIONS_LIMIT = 3
        self._MONSTERS_LIMIT = 10
        self._TICK_MS = 1000
        self._ROOM_SIZE = 23
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

    def distance(self, a, b):
        if self.isRoom(a,b) == True:
            dist = math.fabs(a[0] - b[0]) + math.fabs(a[1] - b[1])
            return dist
        else:
            p = self.which_door(a,b)
            dist = math.fabs(a[0] - p[0]) + math.fabs(a[1] - p[1]) + math.fabs(p[0] - b[0]) + math.fabs(p[1] - b[1])

    # Returns elements of list that fit between minPair and maxPair on both X-axis and Y-axis
    @staticmethod
    def filter(lst, minPair, maxPair):
        newlist = []
        for elem in lst:
            if (elem[0] >= minPair[0]) and (elem[0] <= maxPair[0]):
                if (elem[1] >= minPair[1]) and (elem[1] <= maxPair[1]):
                    newlist.append(elem)
        return newlist

    def rand_cord(self):
        x = random.randint(0, self._WIDTH)
        y = random.randint(0, self._HEIGHT)
        return (x,y)

    def convertToLocal(self, globalCoordinates):
        return (globalCoordinates[0]%(self._ROOM_SIZE+1), globalCoordinates[1]%(self._ROOM_SIZE+1), globalCoordinates[0]/(self._ROOM_SIZE+1), globalCoordinates[1]/(self._ROOM_SIZE)+1)
        #not including walls - we cannot enter walls apart from doors - special case

    def convertToGlobal(self, localCoordinates):
        return (localCoordinates[2]*(self._ROOM_SIZE+1)+localCoordinates[0], localCoordinates[3]*(self._ROOM_SIZE+1)+localCoordinates[1])

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
            if self.distance(ptn, pos) < self._mindist/4:
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

        #random 2 numbers: coordinates of goals, if too close, repeat
    def add_goals(self):
        self._pgoal = self.rand_cord()
        while self.distance(self._pgoal, self._playerPos) > (10 * self._mindist):
            self._pgoal = self.rand_cord()

        self._agoal = self.rand_cord()
        while self.distance(self._agoal, self._playerPos) > (10 * self._mindist) or self.distance(self._agoal, self._pgoal) > (5 * self._mindist):
            self._agoal = self.rand_cord()


    def isRoom(self,a,b):
        #describe doors on the right
        p = math.ceil(a[0]/24)
        q = math.floor(a[1]/24)+12
        righ = (p,q)
        #describe doors on the bottom
        s = math.ceil(a[1]/24)
        r = math.floor(a[0]/24)+12
        botto = (r,s)
        if (self.convertToGlobal(a)[2] == (self.convertToGlobal(b)[2] and self.convertToGlobal(a)[3] == self.convertToGlobal(b)[3]) or righ==b or botto==b):
            return True 
        else:
            return False

    def isneigh(self,a,b):
        if self.convertToGlobal(a)[2]== 1 + self.convertToGlobal(b)[2] or self.convertToGlobal(a)[2]==self.convertToGlobal(b)[2] - 1:
            return True 
        if self.convertToGlobal(a)[3]== 1 + self.convertToGlobal(b)[3] or self.convertToGlobal(a)[3]==self.convertToGlobal(b)[3] - 1:
            return True
        return False

    def link_doors(self,a,b):
        if self.isneigh(a,b)==True:
            #positions of rooms that a,b belong to
            #order DOES matter, from a to b
            #works for walls - special cases. generally cool
            m = self.convertToGlobal(a)[2]
            n = self.convertToGlobal(a)[3]
            p = self.convertToGlobal(b)[2]
            q = self.convertToGlobal(b)[3]

            if m == p:
                y = m* (self._ROOM_SIZE+1) + (self._ROOM_SIZE+1)/2
                if n<=q:
                    x = q * (self._ROOM_SIZE+1)
                else: #n>q
                    x = n * (self._ROOM_SIZE+1)
                return (x,y)
            else: #n==q
                x = n* (self._ROOM_SIZE+1) + (self._ROOM_SIZE+1)/2
                if m<=p:
                    y = p * (self._ROOM_SIZE+1)
                else:
                    y = m * (self._ROOM_SIZE+1)
                return(x,y)

        else:
             self.which_door(a,b)


    #return which door by comparing two options
    def which_door(self,a,b):
            m = a[0]
            n = a[1]
            p = b[0]
            q = b[1]

            if m>=p and n>=q:

                k = m-(self._ROOM_SIZE+1)
                l = n-(self._ROOM_SIZE+1)

                point1 = (k,n)
                point2 = (m,l)

                door1 = self.link_doors(a,point1)
                door2 = self.link_doors(a,point2)

                #add to two distances - one from point to doors and another from doors to target
                dist1 = math.fabs(door1[0] - p) + math.fabs(door1[1] - q) + math.fabs(m - door1[0]) + math.fabs(n - door1[1])
                dist2 = math.fabs(door2[0] - p) + math.fabs(door2[1] - q) + math.fabs(m - door2[0]) + math.fabs(n - door2[1])

                if (dist1 <= dist2):
                    return door1
                else:
                    return door2

            elif m>=p and n<q:

                k = m-(self._ROOM_SIZE+1)
                l = n+(self._ROOM_SIZE+1)

                point1 = (k,n)
                point2 = (m,l)

                door1 = self.link_doors(a,point1)
                door2 = self.link_doors(a,point2)

                #add to two distances - from point to doors and from doors to target
                dist1 = math.fabs(door1[0] - p) + math.fabs(door1[1] - q) + math.fabs(m - door1[0]) + math.fabs(n - door1[1])
                dist2 = math.fabs(door2[0] - p) + math.fabs(door2[1] - q) + math.fabs(m - door2[0]) + math.fabs(n - door2[1])

                if (dist1 <= dist2):
                    return door1
                else:
                    return door2


            elif m<p and n>=q:

                k = m+(self._ROOM_SIZE+1)
                l = n-(self._ROOM_SIZE+1)

                point1 = (k,n)
                point2 = (m,l)

                door1 = self.link_doors(a,point1)
                door2 = self.link_doors(a,point2)

                #add to two distances - from point to doors and from doors to target
                dist1 = math.fabs(door1[0] - p) + math.fabs(door1[1] - q) + math.fabs(m - door1[0]) + math.fabs(n - door1[1])
                dist2 = math.fabs(door2[0] - p) + math.fabs(door2[1] - q) + math.fabs(m - door2[0]) + math.fabs(n - door2[1])

                if (dist1 <= dist2):
                    return door1
                else:
                    return door2

            elif m<p and n<q:

                k = m+(self._ROOM_SIZE+1)
                l = n+(self._ROOM_SIZE+1)

                point1 = (k,n)
                point2 = (m,l)

                door1 = self.link_doors(a,point1)
                door2 = self.link_doors(a,point2)

                #add to two distances - from point to doors and from doors to target
                dist1 = math.fabs(door1[0] - p) + math.fabs(door1[1] - q) + math.fabs(m - door1[0]) + math.fabs(n - door1[1])
                dist2 = math.fabs(door2[0] - p) + math.fabs(door2[1] - q) + math.fabs(m - door2[0]) + math.fabs(n - door2[1])

                if (dist1 <= dist2):
                    return door1
                else:
                    return door2

    # Runs every game tick (e.g. 1 second)
    #f.e. if we are in the very top, up arrow does not make sense
    def tick(self):
        localPlayerPos = self.convertToLocal(self._playerPos)
        if self._move == "up" and self._playerPos[1] > 1:
            (i,j)=(self._playerPos[0], self._playerPos[0] - 1 )
            if i%(self._ROOM_SIZE+1) ==0 or j%(self._ROOM_SIZE+1)==0: #if wall
                if i%(self._ROOM_SIZE+1)==(self._ROOM_SIZE/2+1) and j%(self._ROOM_SIZE+1)==0: #if doors
                    self._playerPos = (self._playerPos[0], self._playerPos[1] - 1)
                elif j%(self._ROOM_SIZE+1)==(self._ROOM_SIZE/2+1) and i%(self._ROOM_SIZE+1)==0: #if doors
                    self._playerPos = (self._playerPos[0], self._playerPos[1] - 1)
            else:
                self._playerPos = (self._playerPos[0], self._playerPos[1] - 1) 

        elif self._move == "down" and self._playerPos[1] < self._HEIGHT-1:
            (i,j)=(self._playerPos[0], self._playerPos[0] + 1 )
            if i%(self._ROOM_SIZE+1) ==0 or j%(self._ROOM_SIZE+1)==0: #if wall
                if i%(self._ROOM_SIZE+1)==(self._ROOM_SIZE/2+1) and j%(self._ROOM_SIZE+1)==0: #if doors
                    self._playerPos = (self._playerPos[0], self._playerPos[1] + 1)
                elif j%(self._ROOM_SIZE+1)==(self._ROOM_SIZE/2+1) and i%(self._ROOM_SIZE+1)==0: #if doors
                    self._playerPos = (self._playerPos[0], self._playerPos[1] + 1)
            else:
                self._playerPos = (self._playerPos[0], self._playerPos[1] + 1) 

        elif self._move == "left" and self._playerPos[0] > 1:
            (i, j) =(self._playerPos[0]-1, self._playerPos[1])
            if i%(self._ROOM_SIZE+1)==0 or j%(self._ROOM_SIZE+1)==0:
                if i%(self._ROOM_SIZE+1)==(self._ROOM_SIZE/2+1) and j%(self._ROOM_SIZE+1)==0:
                    self._playerPos = (self._playerPos[0]-1, self._playerPos[1])
                elif j%(self._ROOM_SIZE+1)==(self._ROOM_SIZE/2+1) and i%(self._ROOM_SIZE+1):
                    self._playerPos = (self._playerPos[0]-1, self._playerPos[1])
            else:
                self._playerPos = (self._playerPos[0] - 1, self._playerPos[1])

        elif self._move == "right" and self._playerPos[0] < self._WIDTH-1:
            (i, j) =(self._playerPos[0]+1, self._playerPos[1])
            if i%(self._ROOM_SIZE+1)==0 or j%(self._ROOM_SIZE+1)==0:
                if i%(self._ROOM_SIZE+1)==(self._ROOM_SIZE/2+1) and j%(self._ROOM_SIZE+1)==0:
                    self._playerPos = (self._playerPos[0]+1, self._playerPos[1])
                elif j%(self._ROOM_SIZE+1)==(self._ROOM_SIZE/2+1) and i%(self._ROOM_SIZE+1):
                    self._playerPos = (self._playerPos[0]+1, self._playerPos[1])
            else:
                self._playerPos = (self._playerPos[0] + 1, self._playerPos[1])

    def draw(self):
        size = width, height = 500, 500
        white = (255, 255, 255)
        red = (255, 0, 0)
        black = (0,0,0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        yellow = (255,255,0)
        screen = pygame.display.set_mode(size)
        for i in range(0, self._ROOM_SIZE+2):
            for j in range(0, self._ROOM_SIZE+2):
                if i%(self._ROOM_SIZE+1) ==0 or j%(self._ROOM_SIZE+1)==0: #if wall
                    if i%(self._ROOM_SIZE+1)==(self._ROOM_SIZE/2+1) and j%(self._ROOM_SIZE+1)==0: #if doors
                        pygame.draw.rect(screen, black, [i*size[0]/(self._ROOM_SIZE+2)+1, j*size[1]/(self._ROOM_SIZE+2)+1, 18, 18])
                    elif j%(self._ROOM_SIZE+1)==(self._ROOM_SIZE/2+1) and i%(self._ROOM_SIZE+1)==0: #if doors
                        pygame.draw.rect(screen, black, [i*size[0]/(self._ROOM_SIZE+2)+1, j*size[1]/(self._ROOM_SIZE+2)+1, 18, 18])
                    else: #print wall
                        pygame.draw.rect(screen, green, [i*size[0]/(self._ROOM_SIZE+2)+1, j*size[1]/(self._ROOM_SIZE+2)+1, 18, 18])
                else:
                    pygame.draw.rect(screen, white, [i*size[0]/(self._ROOM_SIZE+2)+1, j*size[1]/(self._ROOM_SIZE+2)+1, 18, 18])

        for k in range(0, self._ROOM_SIZE+2):
                            pygame.draw.rect(screen, green, [k*size[0]/self._ROOM_SIZE+1, 0, 18, 18])

        for k in range(0, self._ROOM_SIZE+2):
                            pygame.draw.rect(screen, green, [k*size[0]/self._ROOM_SIZE+1, (size[1]-size[1]/(self._ROOM_SIZE+2)-1), 18, 18])

        for k in range(0, self._ROOM_SIZE+2):
                            pygame.draw.rect(screen, green, [0, k*size[0]/self._ROOM_SIZE+1, 18, 18])

        for k in range(0, self._ROOM_SIZE+2):
                            pygame.draw.rect(screen, green, [(size[0]-size[0]/(self._ROOM_SIZE+2)-1), k*size[1]/self._ROOM_SIZE+1, 18, 18])


        player = self.convertToLocal(self._playerPos)
        pygame.draw.circle(screen, blue, [(player[0]*size[0]/(self._ROOM_SIZE+2)+(size[0]/(self._ROOM_SIZE+2)/2)), (player[1]*size[1]/(self._ROOM_SIZE+2))+(size[1]/(self._ROOM_SIZE+2)/2)], 4)
        for monster in self.filter(self._monsters, (player[2]*(self._ROOM_SIZE+1), player[3]*(self._ROOM_SIZE+1)), ((player[2]*(self._ROOM_SIZE+1)+self._ROOM_SIZE), (player[3]*(self._ROOM_SIZE+1)+self._ROOM_SIZE))):
            monsterLocal = self.convertToLocal(monster)
            pygame.draw.circle(screen, red, [(monsterLocal[0]*size[0]/(self._ROOM_SIZE+2)+(size[0]/(self._ROOM_SIZE+2)/2)), (monsterLocal[1]*size[1]/(self._ROOM_SIZE+2))+(size[1]/(self._ROOM_SIZE+2))/2], 4)

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
        #if True:
            self.tick()
            self.draw()

        return True

def main():
    pygame.init()
    game = Game()
    while game.update():
        pass

    pygame.quit()
