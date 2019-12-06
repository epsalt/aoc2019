with open("input.txt") as f:
    line = f.readline()
    prog = [int(n) for n in line.split(",")]


def add(prog, loc, resolved, write):
    prog[write] = sum(resolved)

    return prog, loc + 4


def mul(prog, loc, resolved, write):
    a, b = resolved
    prog[write] = a * b

    return prog, loc + 4


def _input(prog, loc, resolved, write):
    prog[write] = int(input("Enter input: "))

    return prog, loc + 2


def _print(prog, loc, resolved, write):
    print(resolved[0])

    return prog, loc + 2


def jit(prog, loc, resolved, write):
    a, b = resolved

    if a:
        loc = b
    else:
        loc = loc + 3

    return prog, loc


def jif(prog, loc, resolved, write):
    a, b = resolved

    if not a:
        loc = b
    else:
        loc = loc + 3

    return prog, loc


def lt(prog, loc, resolved, write):
    a, b = resolved
    prog[write] = a < b

    return prog, loc + 4


def eq(prog, loc, resolved, write):
    a, b = resolved
    prog[write] = a == b
    
    return prog, loc + 4


def decompose(n):
    padded = str(n).zfill(5)
    modes = [int(i) for i in padded[:3]]
    opcode = int(padded[3:])

    return opcode, modes


def run(prog):
    prog = prog[:]
    loc = 0

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
    }

    while True:
        opcode, modes = decompose(prog[loc])
        if opcode == 99:
            break

        modes.reverse()
        fun, pcount, wb = codes[opcode]

        params = prog[loc + 1 : loc + pcount + 1]
        resolved = [n if mode else prog[n] for n, mode in zip(params, modes)]
        write = prog[loc + wb]

        prog, loc = fun(prog, loc, resolved, write)
