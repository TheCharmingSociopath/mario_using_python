import config
import numpy as np
import objects
import characters
from os import system


frame_row = 40
frame_col = 100
Col = 1000
Row = 1000
matrix = [[ ' ' for i in range(Col)] for j in range(Row)]


def floor():
    for i in range(0, Col, 2):
        for j in range(frame_row - 5, frame_row):
            objects.objects('brick', i, j)     
 

def print_board():
    for i in range(frame_row - 5):
        for j in range(frame_col):
            matrix[i][j] = (config.colors['sky'], ' ', config.colors['end'])

    for i in config.enemies:
        if i.x >= 0 and i.x < frame_col:
            characters.make_enemy(i)

    for i in config.coins:
        if i.x >= 0 and i.x <= frame_col:
            objects.coin(i)
    
    for i in config.springs:
        if i.x>= 0 and i.x <= frame_col:
            objects.spring(i)

    for cloud in config.clouds:
        if cloud.x >= 0 and cloud.x < frame_col:
            objects.cloud(cloud)
    
    for i in config.ditches:
        if i.x >= 0 and i.x < frame_col:
            objects.ditch(i)

    for i in config.lazers:
        if i.x >= 0 and i.x < frame_col:
            objects.lazer(i)

    for i in config.obstacles:
        if i.x >= 0 and i.x < frame_col:
            if i.Type == 'block':
                objects.block(i)
            elif i.Type == 'shroom_block':
                objects.shroom_block(i)
            elif i.Type == 'obstacle':
                objects.obstacle(i)

    if config.mario.y < 15:
            config.mario.u = 4
            config.mario.jump_status = True

    if config.mario.Type == 'mario':
        characters.make_mario(config.mario)
    else:
        characters.make_supermario(config.mario)

    Print()


def Print():
    system('clear')
    print('ASCII Mario', '\tLives: ', config.life, '\tLevel: ', config.level,\
    '\tScore: ', config.getScore(), '\tPlay Time: ', int(config.play_time),\
    '\tCoins: ', config.coins_collected)
    for i in range(frame_row):
        for j in range(frame_col):
            try:
                print(matrix[i][j][0] + matrix[i][j][1] + config.colors['White'] + config.colors['end'], end='')
            except:
                print(matrix[i][j], end='')
        print()


def move(direction):
    for k in range(2):
        if config.mario.check_movement(direction) == False:
            return

        if(direction == 'RIGHT'): #mario moves right
            if config.mario.x == 46:
                for enemy in config.enemies:
                    if enemy.jump_status == 0:
                        enemy.x -= 1
                    elif enemy.y > 33:
                        config.enemies.remove(enemy)

                for cloud in config.clouds:
                    cloud.x -= 1
                    if cloud.x + cloud.width < 0:
                        config.clouds.remove(cloud)

                for i in config.coins:
                    i.x -= 1
                    if i.x < 0:
                        config.coins.remove(i)
                        continue

                for i in config.lazers:
                    i.x -= 1
                    if i.x < 0 or i.x > frame_col:
                        config.lazers.remove(i)
                        continue

                for i in config.springs:
                    i.x -= 1
                    if i.x + i.width < 0:
                        config.springs.remove(i)
                        continue
                
                for i in config.obstacles:
                    i.x -= 1
                    if i.x + i.width < 0:
                        config.obstacles.remove(i)

                for i in config.ditches:
                    if i.x > 0:
                        temp = matrix[frame_row - 5][i.x + i.width][1]
                        for j in range(frame_row - 5, frame_row):
                            matrix[j][i.x + i.width - 2] = (config.colors['bricks'], temp)
                            if temp == ']':
                                matrix[j][i.x + i.width - 1] = (config.colors['bricks'], '[')
                            else:
                                matrix[j][i.x + i.width - 1] = (config.colors['bricks'], ']')
                    i.x -= 1
                    if i.x + i.width < 0:
                        config.ditches.remove(i)


                for i in range(0, frame_col):
                    for j in range(frame_row - 5, frame_row):
                        if matrix[j][i] == (config.colors['bricks'], '['):
                            matrix[j][i] = (config.colors['bricks'], ']')
                        else:
                            matrix[j][i] = (config.colors['bricks'], '[')                
            else:
                config.mario.x += 1


        if(direction == 'LEFT'): #mario moves left
            if config.mario.x > 0:
                config.mario.x -= 2


def powerup(obj):
    if obj.power == 0:
        return
    
    if config.mario.Type == 'mario':
        config.mario = characters.SuperMario(config.mario.x, config.mario.y, 'supermario')
    else:
        config.mario.power = True
    obj.power = 0

def powerdown():
    config.mario = characters.Mario(config.mario.x, config.mario.y, 'mario')
    