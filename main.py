from random import randrange
from termcolor import colored as c
import ctypes
import pathlib

SIZE = 5
bt = (ctypes.c_ubyte * (SIZE * SIZE))
st = (ctypes.c_bool * (SIZE * 2 + 2))
cknaster = ctypes.CDLL(pathlib.Path().absolute() / 'knaster.so')
cknaster.init_board.restype = bt
cknaster.init_scores.restype = st
cknaster.set_cell.argtypes= (bt, ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_ubyte)
cknaster.set_cell.restype = ctypes.c_byte
cknaster.update_score.argtypes = (bt, ctypes.c_ubyte, ctypes.c_ubyte, st)
cknaster.update_score.restype = ctypes.c_ushort
cknaster.finished.argtypes = (bt,)
cknaster.finished.restype = ctypes.c_bool
cknaster.count_points.argtypes= (bt, st)
cknaster.count_points.restype = ctypes.c_ubyte

dice = lambda: randrange(1, 7) + randrange(1, 7)

board = cknaster.init_board()
scores = cknaster.init_scores()

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
        numbers = ' '.join(map(lambda x: space_str(board[y * SIZE + x]), range(SIZE)))
        print(f'{y:2}|{numbers}|{start - y:2}')
    print('  +--------------+')
    print('    0  1  2  3  4 ')

while not cknaster.finished(board):
    d = dice()
    draw()
    x, y = user_input(d)
    cknaster.set_cell(board, x, y, d)
    cknaster.update_score(board, x, y, scores)
    print()

score = cknaster.count_points(board, scores)
print(f'your final score is {score}')
