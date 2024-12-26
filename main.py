from random import randrange
from collections import namedtuple
from termcolor import colored as c

dice = lambda: randrange(1, 7) + randrange(1, 7)
Space = namedtuple('Space', ['value', 'circled'])
SIZE = 5

print(dice())

board = [[Space(0, False) for _ in range(SIZE)] for _ in range(SIZE)]

def empty() -> bool:
    for row in board:
        for space in row:
            if space.value == 0:
                return True
    return False

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

        if board[y][x].value not in (0, value):
            print('space already filled')
            continue

        if board[y][x].circled == True:
            print('space already circled')
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

