from collections import namedtuple
from math import ceil

Chem = namedtuple("chem", ["code", "n"])


def parse(line):
    sides = []
    for side in line.split("=>"):
        pairs = [pair.split() for pair in side.split(",")]
        sides.append([Chem(chemical, int(quantity)) for (quantity, chemical) in pairs])

    return sides


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]
    parsed = [parse(line) for line in lines]
    equations = [(reactants, products[0]) for (reactants, products) in parsed]


def requirements(code, equations, fuel):
    req = []

    for reactants, product in equations:
        for reactant in reactants:
            if reactant.code == code:
                req.append((reactant, product))

    count = 0
    for reactant, product in req:
        if product.code == "FUEL":
            count += reactant.n * fuel
        else:
            nprod = requirements(product.code, equations, fuel)
            coeff = ceil(nprod / product.n)
            count += reactant.n * coeff

    return count


def part1(equations):
    return requirements("ORE", equations, fuel=1)


def part2(equations, target=1e12, right=1e9):
    left = 0

    while left <= right:
        mid = (left + right) // 2
        ore = requirements("ORE", equations, fuel=mid)

        if ore > target:
            right = mid - 1
        else:
            left = mid + 1

    return int(right)
