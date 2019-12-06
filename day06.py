with open("input.txt") as f:
    lines = f.readlines()
    orbits = (line.strip().split(")") for line in lines)


starmap = {parent: child for child, parent in orbits}


def path(planet, starmap):
    parent = starmap.get(planet)

    if not parent:
        return []
    else:
        return [parent] + path(parent, starmap)


def part1(starmap):
    return sum(len(path(planet, starmap)) for planet in starmap.keys())


def part2(starmap, a, b):
    paths = [set(path(planet, starmap)) for planet in [a, b]]

    return len(set.symmetric_difference(*paths))
