import sys
from os import system

level = 0
enemies = []
obstacles = []
ditches = []
clouds = []
mario = None
jump_limit = 22
score = 0
life = 5
play_time = 0
coins_collected = 0
coins = []
springs = []
lazers = []


colors = {
    'Black'            : '\x1b[0;30m',
    'Blue'             : '\x1b[0;34m',
    'Green'            : '\x1b[0;32m',
    'Cyan'             : '\x1b[0;36m',
    'Red'              : '\x1b[0;31m',
    'Purple'           : '\x1b[0;35m',
    'Brown'            : '\x1b[0;33m',
    'Gray'             : '\x1b[0;37m',
    'Dark Gray'        : '\x1b[1;30m',
    'Light Blue'       : '\x1b[1;34m',
    'Light Green'      : '\x1b[1;32m',
    'Light Cyan'       : '\x1b[1;36m',
    'Light Red'        : '\x1b[1;31m',
    'Light Purple'     : '\x1b[1;35m',
    'Yellow'           : '\x1b[1;33m',
    'White'            : '\x1b[1;37m',
    'enemy'            : '\x1b[2;37;41m',
    'smartenemy'       : '\x1b[1;32;40m',
    'mario'            : '\x1b[0;30;45m',
    'supermario'       : '\x1b[6;30;45m',
    'sky'              : '\x1b[0;34;44m',
    'end'              : '\x1b[0m',
    'clouds'           : '\x1b[6;37;47m',
    'bricks'           : '\x1b[0;35;43m',
    'ditch'            : '\x1b[1;32;42m',
    'coin'             : '\x1b[0;33;44m',
    'spring'           : '\x1b[0;31;44m',
    'lazer'            : '\x1b[1;31;44m'
}

character_dim = {
    #(height, width)
    #(y, x)
    'mario' : (2, 2),
    'supermario' : (3, 3),
    'enemy' : (2, 2),
    'smartenemy' : (2, 2)
}

object_dim = {
    #(x, y)
    'brick' : (2, 1),
    'cloud' : (17, 5),
    'block' : (4, 2),
    'shroom_block' : (4,2),
    'ditch' : (10, 5),
    'obstacle' : (6, 4),
    'coin' : (1, 1),
    'spring' : (10, 2),
    'lazer' : (1, 1)
}

character_y = {
    #origional y coordinate for each character
    'mario' : 33,
    'supermario' : 32,
    'enemy' : 33,
    'smartenemy' : 33
}

#------------------INPUT----------------------------------------------------
#---------------------------------------------------------------------------

'''
    Allow certain inputs and translate to easier to read format
    UP : 0
    LEFT : 1
    RIGHT : 2
    LAZER : 3
'''

# key presses
UP, LEFT, RIGHT, LAZER, QUIT = range(5)
DIR = [UP, LEFT, RIGHT]
INVALID = -1

# allowed inputs
_allowed_inputs = {
    UP      : ['w', '\x1b[A'], \
    LEFT    : ['a', '\x1b[D'], \
    RIGHT   : ['d', '\x1b[C'], \
    LAZER    : [' '],           \
    QUIT    : ['q']
}

def get_key(key):
    for x in _allowed_inputs:
        if key in _allowed_inputs[x]:
            return x
    return INVALID


# Gets a single character from standard input.  Does not echo to the screen.
class _Getch:

    def __init__(self):
        self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:


    def __init__(self):
        import tty, sys


    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


_getch = _Getch()


class AlarmException(Exception):
    pass


def alarmHandler(signum, frame):
    raise AlarmException


def get_input(timeout=1):
    import signal
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = _getch()
        signal.alarm(0)
        return text
    except AlarmException:
        pass
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''

#-----------END OF INPUT SECTION-------------------------------------------------

def getScore():
    return int(score + coins_collected * 10 + play_time)