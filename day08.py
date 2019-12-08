from collections import Counter
from itertools import zip_longest

with open("input.txt") as f:
    line = f.readline()
    pixels = [int(n) for n in line.strip()]


def grouper(iterable, n, fillvalue=None):
    # https://docs.python.org/3.8/library/itertools.html#itertools-recipes
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def part1(pixels, width, height):
    size = width * height
    images = grouper(pixels, size)
    counters = []

    for image in images:
        c = Counter()
        for pixel in image:
            c[pixel] += 1
        counters.append(c)

    zero_counts = [c[0] for c in counters]
    most_zeroes = min(zero_counts, key=zero_counts.__getitem__)

    return counters[most_zeroes][1] * counters[most_zeroes][2]


def part2(pixels, width, height):
    size = width * height
    images = grouper(pixels, size)
    output = [2 for pixel in range(size)]

    for image in images:
        for i, pixel in enumerate(image):
            if image[i] != 2 and output[i] == 2:
                output[i] = image[i]

    for row in grouper(output, width):
        for pixel in row:
            glyph = "█" if pixel else " "
            print(glyph, end="")
        print()
