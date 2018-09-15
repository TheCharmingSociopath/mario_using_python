import board
import config
import time


class objects:
    def __init__(self, Type, x, y):
        self.Type = Type
        self.x = x
        self.y = y
        self.height = config.object_dim[Type][1]
        self.width = config.object_dim[Type][0]
        self.spawn_time = time.time()

        if Type == 'brick':
            brick(x, y)
            
        elif Type == 'cloud':
            cloud(self)
        
        elif Type == 'block':
            block(self)
        
        elif Type == 'shroom_block':
            shroom_block(self)
            self.power = 1
        
        elif Type == 'ditch':
            ditch(self)

        elif Type == 'obstacle':
            obstacle(self)
        
        elif Type == 'coin':
            coin(self)

        elif Type == 'spring':
            spring(self)

        elif Type == 'lazer':
            lazer(self)

#--------DRAW OBJECTS------------------#

def brick(x, y):
    board.matrix[y][x] = (config.colors['bricks'], '[')
    board.matrix[y][x + 1] = (config.colors['bricks'], ']')


def cloud(cloud):
    x = cloud.x
    y = cloud.y
    for j in range(5, 13):
        board.matrix[y][x + j] = (config.colors['clouds'], '_')
    
    for j in range(2, 16):
        board.matrix[y + 4][x + j] = (config.colors['clouds'], '_')
    
    board.matrix[y + 1][x + 2] = (config.colors['clouds'], '_')
    board.matrix[y + 1][x + 3] = (config.colors['clouds'], '_')
    board.matrix[y + 1][x + 4] = (config.colors['clouds'], '(')
    board.matrix[y + 1][x + 13] = (config.colors['clouds'], ')')
    board.matrix[y + 2][x + 1] = (config.colors['clouds'], '(')
    board.matrix[y + 2][x + 15] = (config.colors['clouds'], ')')
    board.matrix[y + 3][x] = (config.colors['clouds'], '(')
    board.matrix[y + 3][x + 16] = (config.colors['clouds'], ')')
    board.matrix[y + 4][x + 1] = (config.colors['clouds'], '(')
    board.matrix[y + 4][x + 16] = (config.colors['clouds'], ')')


def block(obj):
    x = obj.x
    y = obj.y
    brick(x, y)
    brick(x + 2, y)
    brick(x, y + 1)
    brick(x + 2, y + 1)


def shroom_block(obj):
    x = obj.x
    y = obj.y
    board.matrix[y][x] = (config.colors['bricks'], '[')
    board.matrix[y][x + 1] = (config.colors['bricks'], '?')
    board.matrix[y][x + 2] = (config.colors['bricks'], '?')
    board.matrix[y][x + 3] = (config.colors['bricks'], ']')
    board.matrix[y + 1][x] = (config.colors['bricks'], '[')
    board.matrix[y + 1][x + 1] = (config.colors['bricks'], '?')
    board.matrix[y + 1][x + 2] = (config.colors['bricks'], '?')
    board.matrix[y + 1][x + 3] = (config.colors['bricks'], ']')
    

def ditch(ditch):
    x = ditch.x
    y = ditch.y

    for i in range(config.object_dim['ditch'][1]):
        for j in range(config.object_dim['ditch'][0]):
            board.matrix[y + i][x + j] = (config.colors['sky'], ' ')

def obstacle(obj):
    x = obj.x
    y = obj.y
    for i in range(0, 6):
        for j in range(0, 4):
            board.matrix[y + j][x + i] = (config.colors['ditch'], '|')

def coin(obj):
    board.matrix[obj.y][obj.x] = (config.colors['coin'], '0')

def spring(obj):
    board.matrix[obj.y][obj.x] = (config.colors['spring'], '|')
    board.matrix[obj.y + 1][obj.x] = (config.colors['spring'], '|')
    board.matrix[obj.y][obj.x + 1] = (config.colors['spring'], '_')
    board.matrix[obj.y][obj.x + 2] = (config.colors['spring'], '_')
    board.matrix[obj.y][obj.x + 3] = (config.colors['spring'], '_')
    board.matrix[obj.y][obj.x + 4] = (config.colors['spring'], '_')
    board.matrix[obj.y][obj.x + 5] = (config.colors['spring'], '_')
    board.matrix[obj.y][obj.x + 6] = (config.colors['spring'], '_')
    board.matrix[obj.y][obj.x + 7] = (config.colors['spring'], '_')
    board.matrix[obj.y][obj.x + 8] = (config.colors['spring'], '_')
    board.matrix[obj.y][obj.x + 9] = (config.colors['spring'], '|')
    board.matrix[obj.y + 1][obj.x + 9] = (config.colors['spring'], '|')

def lazer(obj):
    board.matrix[obj.y][obj.x] = (config.colors['lazer'], '*')