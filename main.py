from random import randrange
from termcolor import colored as c
import ctypes
import pathlib
from collections import namedtuple

SIZE = 5
cknaster = ctypes.CDLL(pathlib.Path().absolute() / 'knaster.so')
cknaster.init_board.restype = ctypes.POINTER(ctypes.c_ubyte)
cknaster.init_scores.restype = ctypes.POINTER(ctypes.c_bool)
cknaster.init_cell_selector = ctypes.POINTER(ctypes.c_bool)
cknaster.set_cell.argtypes = (
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_ubyte,
    ctypes.c_ubyte,
    ctypes.c_ubyte,
    ctypes.POINTER(ctypes.c_bool),
    ctypes.POINTER(ctypes.c_bool)
)
cknaster.set_cell.restype = ctypes.c_byte
cknaster.finished.argtypes = (ctypes.POINTER(ctypes.c_ubyte),)
cknaster.finished.restype = ctypes.c_bool
cknaster.count_points.argtypes= (ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_bool))
cknaster.count_points.restype = ctypes.c_ubyte

dice = lambda: randrange(1, 7) + randrange(1, 7)

Option = namedtuple('Option', ['index', 'text'])

board = cknaster.init_board()
scores = cknaster.init_scores()
selections = cknaster.init_cell_selector()
texts = (
    Option(0, 'row'),
    Option(1, 'column'),
    Option(2, 'up-left to down-right'),
    Option(3, 'up-right to down-left'),
)

def user_input(value: int) -> str:
    while True:
        try:
            x, y = input(f'you have rolled a {value} where do you want to place it? ').strip().split(' ')
        except KeyboardInterrupt:
            print('\nbye')
            exit(0)
        except:
            print('this input is not in the form "x y"')
            continue

        try:
            x, y = int(x), int(y)
        except:
            print('this input is not made up of 2 integers')
            continue

        if not (x >= 0 and x < SIZE
            and y >= 0 and y < SIZE):
            print(f'one of the numbers is not in the range 0 to {SIZE}')
            continue

        return x, y

def space_str(space: int) -> str:
    if space != 0:
        if space >= 128:
            return c(f'{space & 0b1111:2}', 'red')
        else:
            return f'{space:2}'
    else:
        return '  '

def draw():
    print('10  9  8  7  6  5 10')
    print('  +--------------+')
    start = 9
    for y in range(SIZE):
        numbers = ' '.join(space_str(board[y * SIZE + x]) for x in range(SIZE))
        print(f'{y:2}|{numbers}|{start - y:2}')
    print('  +--------------+')
    print('    0  1  2  3  4 ')

while not cknaster.finished(board):
    d = dice()
    draw()
    result = -1
    while result < 0:
        x, y = user_input(d)
        result = cknaster.set_cell(board, x, y, d, scores, selections)
    if result > 0:
        options = []
        for i in range(4):
            if selections[i]:
                options.append(texts[i])

        while len(options) > 0:
            for i, option in enumerate(options):
                print(f'{i}: {option.text}')
            input('choose an option')
            
    print()

score = cknaster.count_points(board, scores)
print(f'your final score is {score}')
