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
    POINTER(c_ubyte),  # board
    POINTER(c_bool),  # field_selectors
)
cknaster.get_fields_for_cell_selection.restype = c_ubyte  # num
cknaster.finished.argtypes = (
    POINTER(c_ubyte),  # board
)
cknaster.finished.restype = c_bool  # finished
cknaster.count_points.argtypes = (
    POINTER(c_ubyte),  # board
    POINTER(c_bool),  # scores
)
cknaster.count_points.restype = c_ubyte  # num points


def dice():
    return randrange(1, 7) + randrange(1, 7)


Option = namedtuple("Option", ("index", "text"))

board = cknaster.init_board()
scores = cknaster.init_scores()
selections = cknaster.init_cell_selector()
fields = cknaster.init_field_selector()
options = (
    Option(0, "row"),
    Option(1, "column"),
    Option(2, "up-left to down-right"),
    Option(3, "up-right to down-left"),
)


def user_input(value: int) -> str:
    while True:
        prompt = f"you have rolled a {value} where do you want to place it? "
        text = input(prompt).strip()
        space = text.index(" ")
        if space != text.rindex(" "):
            print("the input contains multiple spaces")
            continue
        if space == -1:
            print("there is no seperator in the input")
            continue

        x, y = text[:space], text[space + 1 :]
        if not (x.isnumeric() and y.isnumeric()):
            print("this input is not made up of 2 integers")
            continue

        x, y = int(text[:space]), int(text[space + 1 :])
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


def field_for_x_y_c(choice, x, y):
    match choice:
        case 0:
            return range(y * SIZE, y * SIZE + SIZE)
        case 1:
            return range(x, SIZE * SIZE, SIZE)
        case 2:
            return range(0, SIZE * SIZE, SIZE + 1)
        case 3:
            return range(SIZE - 1, SIZE * SIZE, SIZE - 1)
    raise Exception(f"impossible choice {choice}")


def index_for_field(field, choice, x, y): ...


def draw():
    print("10  9  8  7  6  5 10")
    print("  +--------------+")
    start = 9
    for y in range(SIZE):
        numbers = " ".join(space_str(board[y * SIZE + x]) for x in range(SIZE))
        print(f"{y:2}|{numbers}|{start - y:2}")
    print("  +--------------+")
    print("    0  1  2  3  4 ")


def choose(name, num_options):
    while True:
        choice = input(f"choose an option: ")
        if not choice.isnumeric():
            print("choice is not numeric")
            continue
        if len(choice) != 1:
            print("choice is not the right length")
            continue
        choice = int(choice)
        if choice >= len(options):
            print("choice is to big")
            continue
        return choice


while not cknaster.finished(board):
    d = dice()
    draw()
    result = -1
    while result < 0:
        x, y = user_input(d)
        result = cknaster.set_cell(board, x, y, d, scores, selections)
    available_options = []
    for i in range(4):
        if selections[i]:
            available_options.append(selections[i])

    for _ in range(len(options)):
        for i, option in enumerate(available_options):
            print(f"{i}: {option.text}")
        choosen = choose("straight", len(options))
        free_fields = cknaster.get_fields_for_cell_selection(
            choosen, x, y, board, fields
        )
        field_options = []
        for i, idx in enumerate(field_for_x_y_c(choosen, x, y)):
            if fields[idx]:
                field_options.append(i)

        for _ in range(len(field_options)):
            for i, field_option in enumerate(field_options):
                print(f"{i}: {field_option}. field")
            field = choose("field", len(field_options))

    print()

score = cknaster.count_points(board, scores)
print(f"your final score is {score}")
