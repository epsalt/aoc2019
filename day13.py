from collections import defaultdict, namedtuple
import curses
from itertools import zip_longest
from time import sleep

State = namedtuple("State", ["prog", "loc", "rel_base", "inputs", "output"])

with open("input.txt") as f:
    line = f.readline()
    prog = [int(n) for n in line.split(",")]


def add(state, resolved, write):
    prog = state.prog
    prog[write] = sum(resolved)

    return State(prog, state.loc + 4, state.rel_base, state.inputs, None)


def mul(state, resolved, write):
    a, b = resolved

    prog = state.prog
    prog[write] = a * b

    return State(prog, state.loc + 4, state.rel_base, state.inputs, None)


def _input(state, resolved, write):
    prog = state.prog
    prog[write] = int(state.inputs.pop())

    return State(prog, state.loc + 2, state.rel_base, state.inputs, None)


def _print(state, resolved, write):
    output = resolved[0]
    loc = state.loc + 2

    return State(state.prog, loc, state.rel_base, state.inputs, output)


def jit(state, resolved, write):
    a, b = resolved
    loc = state.loc

    if a:
        loc = b
    else:
        loc = loc + 3

    return State(state.prog, loc, state.rel_base, state.inputs, None)


def jif(state, resolved, write):
    a, b = resolved
    loc = state.loc

    if not a:
        loc = b
    else:
        loc = loc + 3

    return State(state.prog, loc, state.rel_base, state.inputs, None)


def lt(state, resolved, write):
    a, b = resolved
    prog = state.prog
    prog[write] = a < b

    return State(prog, state.loc + 4, state.rel_base, state.inputs, None)


def eq(state, resolved, write):
    a, b = resolved
    prog = state.prog
    prog[write] = a == b

    return State(prog, state.loc + 4, state.rel_base, state.inputs, None)


def rel(state, resolved, write):
    rel_base = state.rel_base + resolved[0]

    return State(state.prog, state.loc + 2, rel_base, state.inputs, None)


def decompose(n):
    padded = str(n).zfill(5)
    modes = [int(i) for i in padded[:3]]
    opcode = int(padded[3:])

    return opcode, modes


def resolve_param(state, param, mode):
    if mode == 0:
        resolved = state.prog[param]
    elif mode == 1:
        resolved = param
    elif mode == 2:
        resolved = state.prog[param + state.rel_base]

    return resolved


def resolve_write(state, wb, mode):
    if mode == 0:
        write = state.prog[state.loc + wb]
    elif mode == 2:
        write = state.prog[state.loc + wb] + state.rel_base

    return write


def run(state):
    ## (function, n_params, write mode bit)
    codes = {
        1: (add, 2, 3),
        2: (mul, 2, 3),
        3: (_input, 0, 1),
        4: (_print, 1, 0),
        5: (jit, 2, 0),
        6: (jif, 2, 0),
        7: (lt, 2, 3),
        8: (eq, 2, 3),
        9: (rel, 1, 0),
    }

    while True:
        opcode, modes = decompose(state.prog[state.loc])
        if opcode == 99:
            return None

        modes.reverse()
        fun, pcount, wb = codes[opcode]

        params = state.prog[state.loc + 1 : state.loc + pcount + 1]
        resolved = [
            resolve_param(state, param, mode) for param, mode in zip(params, modes)
        ]

        write_mode = modes[wb - 1]
        write = resolve_write(state, wb, write_mode)

        state = fun(state, resolved, write)

        if state.output is not None:
            return state
        else:
            pass


def grouper(iterable, n, fillvalue=None):
    # https://docs.python.org/3.8/library/itertools.html#itertools-recipes
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def part1(prog, memory=2 ** 8):
    state = State(prog + [0] * memory, 0, 0, None, None)
    board_state = {}
    output = []

    while True:
        state = run(state)

        if state is None:
            break
        else:
            output.append(state.output)

    for x, y, tile_id in grouper(output, 3):
        board_state[(x, y)] = tile_id

    return sum(1 for tile_id in board_state.values() if tile_id == 2)


def update(stdscr, x, y, tid, score):
    tiles = {0: " ", 1: "|", 2: "#", 3: "_", 4: "*"}
    glyph = tiles[tid]
    stdscr.addstr(y, x, glyph)
    stdscr.addstr(25, 0, "Score: {}".format(score))
    sleep(0.01)
    stdscr.refresh()


def next_move(ball, paddle):
    bx, px = ball[0], paddle[0]

    if bx == px:
        move = 0
    elif bx > px:
        move = 1
    else:
        move = -1

    return move


def part2(prog, memory=2 ** 8):
    prog[0] = 2
    state = State(prog + [0] * memory, 0, 0, None, None)
    score = 0

    board_state = defaultdict(int)
    output = []

    ball = None
    paddle = None

    stdscr = curses.initscr()
    curses.delay_output(100)
    curses.noecho()
    curses.cbreak()

    while True:
        state = run(state)

        if state is None:
            break
        else:
            output.append(state.output)

            if len(output) == 3:
                x, y, tid = output

                ## Check for score and update screen
                if x == -1:
                    score = tid
                else:
                    board_state[(x, y)] = tid
                    update(stdscr, x, y, tid, score)

                ## Check for ball or paddle
                if tid == 4:
                    ball = (x, y)
                elif tid == 3:
                    paddle = (x, y)

                if ball is not None and paddle is not None:
                    move = next_move(ball, paddle)
                else:
                    move = None

                ## Clear output and update state
                output = []
                state = State(state.prog, state.loc, state.rel_base, [move], None)

            else:
                pass

    curses.echo()
    curses.nocbreak()
    curses.endwin()

    return board_state, score


if __name__ == "__main__":
    board_state, score = part2(prog)
    print("Final score {}".format(score))
