from collections import deque, namedtuple

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


def step(state, direction):
    inputs = [direction]
    new = State(state.prog[:], state.loc, state.rel_base, inputs, None)
    response = run(new)

    return response.output, response


def bfs(prog, resp=2):
    init = (complex(0, 0), [], State(prog[:], 0, 0, None, None))
    queue = deque([init])
    visited = {}
    board = {complex(0, 0): 1}

    directions = {
        1: complex(0, 1),
        2: complex(0, -1),
        3: complex(-1, 0),
        4: complex(1, 0),
    }

    while queue:
        curr = queue.pop()
        loc, path, state = curr
        visited[loc] = True

        for code, direction in directions.items():
            nloc = loc + direction
            if visited.get(nloc) is not None:
                pass
            else:
                response, nstate = step(state, code)
                board[nloc] = response

                if response == resp:
                    return path + [loc]
                elif response == 1:
                    queue.appendleft((nloc, path + [loc], nstate))

    return board


def flood(oxygenated, board):
    directions = [
        complex(0, 1),
        complex(0, -1),
        complex(-1, 0),
        complex(1, 0),
    ]

    new = []
    for coord in oxygenated:
        for direction in directions:
            neighbour = coord + direction
            if board[neighbour] == 1:
                board[neighbour] = 2
                new.append(neighbour)
            else:
                pass

    return oxygenated + new, board


def part1(prog):
    return len(bfs(prog, resp=2))


def part2(prog):
    board = bfs(prog, resp=99)
    todo = sum(1 for key, value in board.items() if value == 1)
    oxygenated = [key for key, value in board.items() if value == 2]
    minutes = 0

    while todo - len(oxygenated) + 1 > 0:
        oxygenated, board = flood(oxygenated, board)
        minutes += 1

    return minutes
