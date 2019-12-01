import math

with open("input.txt") as f:
    modules = [int(line.strip()) for line in f.readlines()]


def fuel(n):
    return math.floor(n / 3) - 2


def rec_fuel(mass):
    curr = fuel(mass)
    if curr < 0:
        return 0
    else:
        return curr + rec_fuel(curr)


def part1(modules):
    return sum([fuel(mass) for mass in modules])


def part2(modules):
    return sum([rec_fuel(mass) for mass in modules])
