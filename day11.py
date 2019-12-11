from collections import defaultdict, namedtuple

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


def rotate(heading, clockwise):
    if clockwise:
        return complex(heading.imag, -heading.real)
    else:
        return complex(-heading.imag, heading.real)


def robot(prog, init, memory=2 ** 10):
    hull = defaultdict(bool)
    inputs = []

    # Initial robot position
    pos = 0 + 0j
    direction = 0 + 1j
    hull[pos] = init

    # Initialize program state
    state = State(prog + [0] * memory, 0, 0, inputs, None)

    while True:
        state.inputs.append(hull[pos])
        state = run(state)

        if state is None:
            return hull
        else:
            hull[pos] = state.output
            state = run(state)

            clockwise = state.output
            direction = rotate(direction, clockwise)
            pos += direction


def part1(prog, init=0):
    hull = robot(prog, init)
    return len(hull.keys())


def part2(prog, init=1):
    hull = robot(prog, init)

    xs = [coord.real for coord in hull.keys()]
    ys = [coord.imag for coord in hull.keys()]
    pad = 2

    xbounds = [int(bound) for bound in [min(xs) - pad, max(xs) + pad]]
    ybounds = [int(bound) for bound in [max(ys) + pad, min(ys) - pad]]

    for y in range(*ybounds, -1):
        for x in range(*xbounds):
            pixel = hull[complex(x, y)]
            glyph = "█" if pixel else " "
            print(glyph, end="")
        print()
