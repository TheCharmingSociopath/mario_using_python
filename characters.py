import config
import board
import time
from os import system
import sys


class character:
    def __init__(self, x, y, Type):
        self.x = x
        self.y = y
        self.width = config.character_dim[Type][1]
        self.height = config.character_dim[Type][0]
        self.Type = Type
        self.jump_status = False
        self.u = 0


    def jump(self):
        self.y += self.u
        self.u += 1
        for i in range(self.height):
            for j in range(self.width):
                try:
                    temp = board.matrix[self.y + i][self.x + j][1]
                    if temp == '[' or temp == ']' or temp == '?' or temp == '|':
                        if self.u > 0:
                            self.y = config.character_y[self.Type]
                            self.jump_status = False
                            return
                        else:
                            #break the brick
                            self.y += i
                            self.jump_status = True
                            self.u = 2
                            for i in config.obstacles:
                                temp = i.x - self.x
                                if temp in range(- (self.width - 1), i.width):
                                    if i.Type == 'block' and self.Type == 'supermario':
                                        config.obstacles.remove(i)
                                    elif i.Type == 'shroom_block':
                                        board.powerup(i)
                            return
                except:
                    return
                        

    def check_bottom(self):
        for i in range(self.width):
            temp = board.matrix[self.y + self.height][self.x + i][1]
            if temp == '0':
                temp = board.matrix[self.y + self.height + 1][self.x + i][1]
            if temp == '[' or temp == ']' or temp == '?' or temp == '|':
                self.jump_status = False
                return
            else:
                if self.jump_status == False:
                    self.jump_status = True
                    self.u = 3


class Mario(character):
    def check_movement(self, dir):
        if dir == 'LEFT':
            for i in config.obstacles:
                if self.x == i.x + i.width and i.y + i.height - 1 >= self.y\
                and i.y <= self.y + self.height - 1:
                    return False
            return True
        else:
            for i in config.obstacles:
                if self.x + self.width == i.x and i.y + i.height - 1 >= self.y\
                and i.y <= self.y + self.height - 1:
                    return False
            return True


class SuperMario(Mario):
    def __init__(self, x, y, Type):
        self.power = False
        super().__init__(x, y, Type)


class Enemy(character):
    def __init__(self, x, y, Type):
        super().__init__(x, y, Type)
        # make_enemy(x, y)
        self.spawn_time = time.time()
        self.dir = 'left'


    def check_movement(self):
        if self.dir == 'left':
            for i in config.obstacles:
                if self.x == i.x + i.width and i.y + i.height - 1 >= self.y\
                and i.y <= self.y + self.height - 1:
                    self.dir = 'right'
        else:
            for i in config.obstacles:
                if self.x + self.width == i.x and i.y + i.height - 1 >= self.y\
                and i.y <= self.y + self.height - 1:
                    self.dir = 'left'


    def move_enemy(self):
        self.check_movement()

        if self.dir == 'left':
            self.x -= 1
        else:
            self.x += 1


class SmartEnemy(Enemy):
    def move_enemy(self):
        if config.mario.x < self.x:
            self.dir = 'left'
        else:
            self.dir = 'right'

        self.check_movement()

        if self.dir == 'left':
            self.x -= 1
        else:
            self.x += 1


#--------DRAW CHARACTERS------------------#

def make_mario(mario):
    x = mario.x
    y = mario.y
    for i in range(x, x + config.character_dim['mario'][1]):
        for j in range(y, y + config.character_dim['mario'][0]):
            board.matrix[j][i] = (config.colors['mario'], 'M')


def make_supermario(mario):
    x = mario.x
    y = mario.y
    for i in range(x, x + config.character_dim['supermario'][1]):
        for j in range(y, y + config.character_dim['supermario'][1]):
            board.matrix[j][i] = (config.colors['supermario'], 'M')


def make_enemy(enemy):
    if enemy.Type == 'enemy':
        for i in range(enemy.height):
            for j in range(enemy.width):
                board.matrix[i + enemy.y][j + enemy.x] = (config.colors['enemy'], 'E')
    elif enemy.Type == 'smartenemy':
        board.matrix[enemy.y][enemy.x] = (config.colors['smartenemy'], 'S')
        board.matrix[enemy.y][enemy.x + 1] = (config.colors['smartenemy'], 'E')
        board.matrix[enemy.y + 1][enemy.x] = (config.colors['smartenemy'], 'S')
        board.matrix[enemy.y + 1][enemy.x + 1] = (config.colors['smartenemy'], 'E')
