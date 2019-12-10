from collections import defaultdict
from cmath import phase, rect
from itertools import cycle
from math import pi

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def parse(lines):
    asteroids = []
    for row, line in enumerate(lines):
        for col, position in enumerate(line):
            if position == "#":
                asteroids.append(complex(col, row))

    return asteroids


def scan(station, asteroids):
    results = defaultdict(list)

    for asteroid in asteroids:
        distance = abs(station - asteroid)
        phi = phase(asteroid - station)

        if distance:
            results[phi].append(distance)

    return results


def part1(lines):
    asteroids = parse(lines)
    results = {}

    for station in asteroids:
        count = len(scan(station, asteroids))
        results[station] = count

    return max(results.values()), max(results, key=results.get)


def part2(lines, best, n):
    asteroids = parse(lines)
    stats = scan(best, asteroids)

    for phi in stats:
        stats[phi].sort(reverse=True)

    angles = [key for key in stats.keys()]
    angles.sort()

    up = angles.index(-pi / 2)
    order = cycle(angles[up:] + angles[:up])

    shots = 1
    while shots <= n:
        phi = next(order)

        if stats[phi]:
            dist = stats[phi].pop()
            shots += 1
        else:
            pass

    nth = rect(dist, phi) + best

    return round(nth.real * 100 + nth.imag)
