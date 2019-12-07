from itertools import cycle, permutations

with open("input.txt") as f:
    line = f.readline()
    prog = [int(n) for n in line.split(",")]


def add(prog, loc, resolved, write, inputs):
    prog[write] = sum(resolved)

    return prog, loc + 4


def mul(prog, loc, resolved, write, inputs):
    a, b = resolved
    prog[write] = a * b

    return prog, loc + 4


def _input(prog, loc, resolved, write, inputs):
    message = inputs.pop(0)
    prog[write] = int(message)

    return prog, loc + 2


def _print(prog, loc, resolved, write, inputs):
    return prog, loc + 2


def jit(prog, loc, resolved, write, inputs):
    a, b = resolved

    if a:
        loc = b
    else:
        loc = loc + 3

    return prog, loc


def jif(prog, loc, resolved, write, inputs):
    a, b = resolved

    if not a:
        loc = b
    else:
        loc = loc + 3

    return prog, loc


def lt(prog, loc, resolved, write, inputs):
    a, b = resolved
    prog[write] = a < b

    return prog, loc + 4


def eq(prog, loc, resolved, write, inputs):
    a, b = resolved
    prog[write] = a == b

    return prog, loc + 4


def decompose(n):
    padded = str(n).zfill(5)
    modes = [int(i) for i in padded[:3]]
    opcode = int(padded[3:])

    return opcode, modes


def run(prog, loc, inputs):
    prog = prog[:]
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
            return prog, None, None

        modes.reverse()
        fun, pcount, wb = codes[opcode]

        params = prog[loc + 1 : loc + pcount + 1]
        resolved = [n if mode else prog[n] for n, mode in zip(params, modes)]
        write = prog[loc + wb]

        prog, loc = fun(prog, loc, resolved, write, inputs)

        if fun == _print:
            output = resolved[0]
            return prog, loc, output


def amplify(prog, signals):
    message = 0
    loc = 0

    for signal in signals:
        stack = [signal, message]
        _, _, message = run(prog, 0, stack)

    return message


def amplify_feedback(prog, signals, init=0):
    states = [{"prog": prog[:], "stack": [signal], "loc": 0} for signal in signals]
    loop = cycle(states)

    message = init

    while True:
        state = next(loop)

        if state["loc"] is None:
            break

        else:
            state["stack"].append(message)
            returns = run(state["prog"], state["loc"], state["stack"])
            state["prog"], state["loc"], message = returns

        if message:
            result = message

    return result


def part1(prog):
    signals = (amplify(prog, combo) for combo in permutations("01234"))

    return max(signals)


def part2(prog):
    signals = (amplify_feedback(prog, combo) for combo in permutations("56789"))

    return max(signals)
