from collections import namedtuple

State = namedtuple("State", ["prog", "loc", "rel_base"])

with open("input.txt") as f:
    line = f.readline()
    prog = [int(n) for n in line.split(",")]


def add(state, resolved, write):
    prog = state.prog
    prog[write] = sum(resolved)

    return State(prog, state.loc + 4, state.rel_base)


def mul(state, resolved, write):
    a, b = resolved

    prog = state.prog
    prog[write] = a * b

    return State(prog, state.loc + 4, state.rel_base)


def _input(state, resolved, write):
    prog = state.prog
    prog[write] = int(input("Enter input: "))

    return State(prog, state.loc + 2, state.rel_base)


def _print(state, resolved, write):
    print(resolved[0])

    return State(state.prog, state.loc + 2, state.rel_base)


def jit(state, resolved, write):
    a, b = resolved
    loc = state.loc

    if a:
        loc = b
    else:
        loc = loc + 3

    return State(state.prog, loc, state.rel_base)


def jif(state, resolved, write):
    a, b = resolved
    loc = state.loc

    if not a:
        loc = b
    else:
        loc = loc + 3

    return State(state.prog, loc, state.rel_base)


def eq(state, resolved, write):
    a, b = resolved
    prog = state.prog
    prog[write] = a == b

    return State(prog, state.loc + 4, state.rel_base)


def rel(state, resolved, write):
    rel_base = state.rel_base + resolved[0]
    
    return State(state.prog, state.loc + 2, rel_base)


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


def run(prog, memory=2 ** 10):
    state = State(prog[:] + [0] * memory, 0, 0)

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
            break

        modes.reverse()
        fun, pcount, wb = codes[opcode]

        params = state.prog[state.loc + 1 : state.loc + pcount + 1]
        resolved = [
            resolve_param(state, param, mode) for param, mode in zip(params, modes)
        ]

        write_mode = modes[wb - 1]
        write = resolve_write(state, wb, write_mode)

        state = fun(state, resolved, write)
