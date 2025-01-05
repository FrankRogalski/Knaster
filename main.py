from random import randrange
from termcolor import colored as c
from ctypes import POINTER, CDLL, c_ubyte, c_bool, c_byte
import pathlib
from collections import namedtuple

SIZE = 5
cknaster = CDLL(pathlib.Path().absolute() / "knaster.so")
cknaster.init_board.restype = POINTER(c_ubyte)  # board
cknaster.init_scores.restype = POINTER(c_bool)  # scores
cknaster.init_cell_selector.restype = POINTER(c_bool)  # cell selectors
cknaster.init_field_selector.restype = POINTER(c_bool)  # field selectors
cknaster.set_cell.argtypes = (
    POINTER(c_ubyte),  # board
    c_ubyte,  # x
    c_ubyte,  # y
    c_ubyte,  # value
    POINTER(c_bool),  # scores
    POINTER(c_bool),  # cell_selector
)
cknaster.set_cell.restype = c_byte  # error code
cknaster.get_fields_for_cell_selection.argtypes = (
    c_ubyte,  # cell selection
    c_ubyte,  # x
    c_ubyte,  # y
    POINTER(c_ubyte),  # fields
    POINTER(c_ubyte),  # board
    POINTER(c_bool),  # field_selectors
)
cknaster.get_fields_for_cell_selection.restype = c_ubyte  # num
cknaster.finished.argtypes = (
    POINTER(c_ubyte),  # board
)
cknaster.finished.restype = c_bool  # finished
cknaster.count_points.argtypes = (
    POINTER(c_ubyte),
    POINTER(c_bool),
)
cknaster.count_points.restype = c_ubyte  # num points

dice = lambda: randrange(1, 7) + randrange(1, 7)

Option = namedtuple("Option", ("index", "text"))

board = cknaster.init_board()
scores = cknaster.init_scores()
selections = cknaster.init_cell_selector()
options = (
    Option(0, "row"),
    Option(1, "column"),
    Option(2, "up-left to down-right"),
    Option(3, "up-right to down-left"),
)


def user_input(value: int) -> str:
    while True:
        try:
            x, y = (
                input(f"you have rolled a {value} where do you want to place it? ")
                .strip()
                .split(" ")
            )
        except KeyboardInterrupt:
            print("\nbye")
            exit(0)
        except:
            print('this input is not in the form "x y"')
            continue

        try:
            x, y = int(x), int(y)
        except:
            print("this input is not made up of 2 integers")
            continue

        if not (x >= 0 and x < SIZE and y >= 0 and y < SIZE):
            print(f"one of the numbers is not in the range 0 to {SIZE}")
            continue

        return x, y


def space_str(space: int) -> str:
    if space != 0:
        if space >= 128:
            return c(f"{space & 0b1111:2}", "red")
        else:
            return f"{space:2}"
    else:
        return "  "


def draw():
    print("10  9  8  7  6  5 10")
    print("  +--------------+")
    start = 9
    for y in range(SIZE):
        numbers = " ".join(space_str(board[y * SIZE + x]) for x in range(SIZE))
        print(f"{y:2}|{numbers}|{start - y:2}")
    print("  +--------------+")
    print("    0  1  2  3  4 ")


while not cknaster.finished(board):
    d = dice()
    draw()
    result = -1
    while result < 0:
        x, y = user_input(d)
        result = cknaster.set_cell(board, x, y, d, scores, selections)
    if result == 0:
        available_options = []
        for i in range(4):
            if selections[i]:
                available_options.append(texts[i])

        while len(options) > 0:
            for i, option in enumerate(available_options):
                print(f"{i}: {option.text}")
            choosen = None
            while True:
                choice = input('choose an option: ')
                if not choice.isnumeric():
                    print('choice is not numeric')
                    continue
                if len(choice) != 1:
                    print('choice is not the right length')
                    continue
                choice = int(choice)
                if choice >= len(options):
                    print('choice is to big')
                    continue
                choosen = choice
            #TODO: continue working
            cknaster.get_fields_for_cell_selection


                    

    print()

score = cknaster.count_points(board, scores)
print(f"your final score is {score}")
