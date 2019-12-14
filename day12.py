from collections import namedtuple
from itertools import combinations
from math import gcd
import re

Moon = namedtuple("Moon", ["name", "pos", "vel"])
XYZ = namedtuple("XYZ", ["x", "y", "z"])
names = ["Io", "Europa", "Ganymede", "Callisto"]


def parse(line):
    pattern = r"=(-?\d+)[\n\s]*"
    matches = re.findall(pattern, line)

    return map(int, matches)


with open("input.txt") as f:
    lines = f.readlines()
    args = (parse(line) for line in lines)
    state = [
        Moon(name, XYZ(*positions), XYZ(0, 0, 0))
        for positions, name in zip(args, names)
    ]


def compare(a, b):
    new = []
    for axis in range(3):
        ai, bi = a[axis], b[axis]

        if ai == bi:
            d = 0
        else:
            d = 1 if ai < bi else -1

        new.append(d)

    return XYZ(*new)


def step(state):
    moons = {moon.name: moon for moon in state}

    ## Update velocity
    for a, b in combinations(state, 2):
        ad = compare(a.pos, b.pos)
        bd = XYZ(-ad.x, -ad.y, -ad.z)

        for moon, d in zip((a, b), (ad, bd)):
            old = moons[moon.name].vel
            new = XYZ(old.x + d.x, old.y + d.y, old.z + d.z)

            moons[moon.name] = Moon(moon.name, moon.pos, new)

    ## Update position and yield
    new_moons = []
    for moon in moons.values():
        pos = XYZ(
            moon.pos.x + moon.vel.x, moon.pos.y + moon.vel.y, moon.pos.z + moon.vel.z
        )

        new_moons.append(Moon(moon.name, pos, moon.vel))

    return new_moons


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def part1(state, steps):
    curr = 0
    while curr < steps:
        state = step(state)
        curr += 1

    total = 0
    for moon in state:
        pot = sum(abs(moon.pos[i]) for i in range(3))
        kin = sum(abs(moon.vel[i]) for i in range(3))
        total += pot * kin

    return total


def part2(state):
    init = {moon.name: moon for moon in state}
    found = {}
    todo = (0, 1, 2)

    n = 0
    while todo:
        n += 1
        state = step(state)

        for axis in todo:
            pos = [moon.pos[axis] == init[moon.name].pos[axis] for moon in state]
            vel = [moon.vel[axis] == init[moon.name].vel[axis] for moon in state]

            if all(pos) and all(vel):
                todo = tuple(i for i in todo if i != axis)
                found[axis] = n

                print(["x", "y", "z"][axis], ":", n)

    return lcm(lcm(found[0], found[1]), found[2])
