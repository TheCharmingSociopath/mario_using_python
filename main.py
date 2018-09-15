import random
from os import system
import time
import numpy as np
import board
import characters
import config
import sys
import objects


def initialize():
    del config.enemies[:]
    del config.obstacles[:]
    del config.ditches[:]
    del config.clouds[:]
    del config.mario
    del config.coins[:]


    system('clear')
    board.floor()
    config.clouds.append(objects.objects('cloud', 10, 2))
    config.clouds.append(objects.objects('cloud', 50, 2))

    config.mario = characters.Mario(2, 33, 'mario')

    config.obstacles.append(objects.objects('block', 21, 28))
    config.obstacles.append(objects.objects('shroom_block', 25, 28))
    config.obstacles.append(objects.objects('block', 29, 28))

    config.ditches.append(objects.objects('ditch', 120, 35))

    config.enemies.append(characters.Enemy(80, 33, 'enemy'))

    board.print_board()


def die():
    if config.life > 0:
        config.life -= 1
        initialize()
        return
    system('clear')
    print('Score: ', config.getScore())
    print('Time Played: ', int(config.play_time))
    sys.exit(0)


def main():
    start_time = time.time()
    level_time = start_time
    bridge_spawntime = start_time

    initialize()

    while True:

        curr_time = time.time()
        config.score += 1
        config.play_time = curr_time - start_time

        if curr_time - level_time > 40:
            config.level += 1
            level_time = curr_time
            print('Level: ', config.level)
            
    #-----------ENEMY-----------------------------------------------------
        if config.level < 3:
            if len(config.enemies) == 0 or (int(curr_time - config.\
            enemies[-1].spawn_time) > 7 - config.level and len(config.enemies) < 8):
                rand_x = random.randint(100, 115)
                config.enemies.append(characters.Enemy(rand_x, 33, 'enemy'))
        
        else:
            if len(config.enemies) == 0 or (int(curr_time - config.\
            enemies[-1].spawn_time) > 7 - config.level and len(config.enemies) < 4):
                rand_x = random.randint(100, 115)
                config.enemies.append(characters.SmartEnemy(rand_x, 33, 'smartenemy'))

        for enemy in config.enemies:
            enemy.move_enemy()

            if enemy.x < 0 or enemy.y > 33:
                config.enemies.remove(enemy)
                continue

            enemy.check_bottom()
            if enemy.jump_status == True:
                enemy.u = 1
                enemy.jump()

            if config.mario.y + config.mario.height - 1 < enemy.y:
                continue

            temp = enemy.x - config.mario.x
            if temp in range(-2, 2):
                if config.mario.jump_status == True and enemy.Type == 'enemy':
                    config.enemies.remove(enemy)
                    config.score += 50
                else:
                    if config.mario.Type == 'mario':
                        die()
                    else:
                        board.powerdown()
                        config.enemies.remove(enemy)
                        continue

    #-----------END OF ENEMY-----------------------------------------------------

        config.mario.check_bottom()

    #-----------INPUT------------------------------------------------------------
        inp = config.get_key(config.get_input())

        if inp == 0: #up
            if config.mario.jump_status == False:
                config.mario.jump_status = True
                config.mario.u = -4

        elif inp == 1: #left
            board.move('LEFT')

        elif inp == 2: #right
            board.move('RIGHT')
            if len(config.clouds) == 0 or config.clouds[-1].x < 75 - random.randint(0, 5):
                config.clouds.append(objects.objects('cloud', 100, random.randint(0, 2)))

        elif inp == 3: #lazer
            if config.mario.Type == 'supermario' and config.mario.power == True:
                x = config.mario.x + config.mario.width
                y = config.mario.y + config.mario.height - 1
                config.lazers.append(objects.objects('lazer', x, y))
                
        elif inp == 4: #quit
            system('clear')
            print('Score: ', config.getScore())
            print('Time Played: ', int(config.play_time))
            sys.exit(0)

    #----------END OF INPUT SECTION-------------------------------------------------
   
    #----------HANDLE MARIO------------------------------------------------------
        
        if config.mario.y > config.character_y[config.mario.Type]:
            die()
        
        for i in config.coins:
            if i.x >= 0 and i.x <= board.frame_col:
                try:
                    if board.matrix[i.y][i.x][1] == 'M':
                        config.coins_collected += 1
                        config.coins.remove(i)
                        continue
                except:
                    pass        

        for i in config.springs:
            if config.mario.x > i.x and config.mario.x + config.mario.width < i.x + i.width\
            and config.mario.y - i.y <= config.mario.height and config.mario.jump_status == True:
                config.mario.y -= 6
                config.mario.u = -4

        if config.mario.jump_status == True:
            config.mario.jump()

        for i in config.lazers:
            i.x += 3
            flag = False
            for j in config.obstacles:
                if i.x in range(j.x, j.x + j.width - 1) and i.y >= j.y and j.Type == 'obstacle':
                    flag = True
                    break

            if flag == True:
                config.lazers.remove(i)
                continue
            
            for j in config.enemies:
                if i.x - j.x in range(-1, 1):
                    config.enemies.remove(j)
                    config.lazers.remove(i)
                    config.score += 20
                    break

    #-----------END OF HANDLE MARIO SECTION--------------------------------------

    #-----------GENERATING OBSTACLES-------------------------------------------------
        rand_x = random.randint(115, 120)
        if len(config.ditches) == 0 or curr_time - config.ditches[-1].spawn_time > 20 - min(config.level, 5):
            config.ditches.append(objects.objects('ditch', rand_x, 35))
        
            if config.level > 5 and random.randint(1, 5) == 2:
                config.springs.append(objects.objects('spring', rand_x - 10, 33))

        rand_x = random.randint(140, 150)
        if len(config.obstacles) == 0 or curr_time - config.obstacles[-1].spawn_time > 20 - min(config.level, 5):
            config.obstacles.append(objects.objects('obstacle', rand_x - 8, 31))

        rand_x = random.randint(135, 140)
        if curr_time - bridge_spawntime > 20:
            bridge_spawntime = curr_time
            number_of_blocks = random.randint(8, 20)

            for i in range(number_of_blocks):
                if i == int(number_of_blocks / 2):
                    config.obstacles.append(objects.objects('shroom_block', rand_x + (i * 4), 28))
                else:
                    config.obstacles.append(objects.objects('block', rand_x + (i * 4), 28))

            for i in range(0, number_of_blocks * 4, 2):
                config.coins.append(objects.objects('coin', rand_x + i, 27))

        board.print_board()

           
    #-----------END OF OBSTACLE GENERATION-------------------------------------------

if __name__ == '__main__':
    main()
