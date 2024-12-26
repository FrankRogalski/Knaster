from random import randrange
from termcolor import colored as c
import ctypes
import pathlib

cknaster =ctypes.CDLL(pathlib.Path().absolute() / 'knaster.so')
cknaster.init_board.restype = ctypes.c_char_p
cknaster.init_scores.restype = ctypes.c_char_p
cknaster.set_cell.argtypes= (ctypes.c_char_p, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte)
cknaster.set_cell.restype = ctypes.c_byte
cknaster.update_score.argtypes = (ctypes.c_char_p, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_char_p)
cknaster.update_score.restype = ctypes.c_ushort
cknaster.finished.argtypes = (ctypes.c_char_p,)
cknaster.finished.restype = ctypes.c_bool
cknaster.count_points.argtypes= (ctypes.c_char_p, ctypes.c_char_p)
cknaster.count_points.restype = ctypes.c_ubyte

dice = lambda: randrange(1, 7) + randrange(1, 7)
SIZE = 5

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

def space_str(space: Space) -> str:
    if space.value != 0:
        if space.circled:
            return c(f'{space.value:2}', 'red')
        else:
            return f'{space.value:2}'
    else:
        return '  '

def draw():
    print('10  9  8  7  6  5 10')
    print('  +--------------+')
    start = 9
    for i, row in enumerate(board):
        numbers = ' '.join(map(space_str, row))
        print(f'{i:2}|{numbers}|{start - i:2}')
    print('  +--------------+')
    print('    0  1  2  3  4 ')

while empty():
    d = dice()
    draw()
    x, y = user_input(d)
    board[y][x] = Space(d, board[y][x].value != 0)
    print()

