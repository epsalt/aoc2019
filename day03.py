with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]


def coord(step):
    direction = "".join(char for char in step if char.isalpha())
    distance = int("".join(char for char in step if char.isdigit()))

    complexifier = {
        "U": complex(0, 1),
        "D": complex(0, -1),
        "L": complex(1, 0),
        "R": complex(-1, 0),
    }

    return (complexifier[direction], distance)


wires = [map(coord, line.split(",")) for line in lines]


def walk(wire):
    path = []
    loc = 0

    for coord in wire:
        direction, distance = coord
        for step in range(distance):
            loc += direction
            path.append(loc)

    return path


def part1(wires):
    routes = [set(walk(wire)) for wire in wires]
    intersections = set.intersection(*routes)
    closest = min(abs(n.real) + abs(n.imag) for n in intersections)
    return int(closest)


def part2(wires):
    routes = [walk(wire) for wire in wires]
    intersections = set.intersection(*[set(route) for route in routes])

    counts = []
    for intersect in intersections:
        steps = sum(route.index(intersect) + 1 for route in routes)
        counts.append(steps)

    return min(counts)
