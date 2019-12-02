from itertools import product, zip_longest
from operator import add, mul

with open("input.txt") as f:
    line = f.readline()
    prog = [int(n) for n in line.split(",")]

codes = {1: add, 2: mul}


def grouper(iterable, n, fillvalue=None):
    # https://docs.python.org/3.8/library/itertools.html#itertools-recipes
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def run(oprog, stop=99):
    prog = oprog[:]
    groups = grouper(prog, 4)
    for group in groups:
        code, a, b, out = group
        if code == stop:
            break
        else:
            op = codes[code]
            prog[out] = op(prog[a], prog[b])
    return prog[0]


def part1(prog, noun, verb):
    prog[1], prog[2] = noun, verb
    return run(prog)


def part2(prog, goal):
    for comb in product(range(100), range(100)):
        noun, verb = comb
        prog[1], prog[2] = noun, verb

        if run(prog) == goal:
            return 100 * noun + verb
