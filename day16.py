from itertools import count, cycle, islice
from collections import deque

with open("input.txt") as f:
    signal = (int(n) for n in f.readline().strip())


def phase(signal):
    queue = deque(signal)
    pattern = (1, 0, -1, 0)
    for i in count(start=1):
        if queue:
            coeffs = cycle(x for x in pattern for y in range(i))
            print([next(coeffs) for d in queue])
            yield abs(sum(d * next(coeffs) for d in queue)) % 10
            queue.popleft()
        else:
            break


def csum(signal, offset):
    cyc = cycle(signal)

    n = total = 0
    new = []
    while n < offset:
        total += next(cyc)
        new.append(total % 10)
        n += 1

    return new


def part1(signal, phases):
    for i in count(1):
        if i > phases:
            break
        else:
            signal = phase(signal)
    return "".join(str(digit) for digit in islice(signal, 8))


def part2(signal, repeats=10000, phases=100):
    signal = list(signal)
    repeated_length = repeats * len(signal)
    offset = int("".join(str(digit) for digit in signal[:7]))

    signal = reversed(signal)
    n = 0
    while n < phases:
        signal = csum(signal, repeated_length - offset)
        n += 1

    return "".join(str(digit) for digit in (reversed(signal[-8:])))
