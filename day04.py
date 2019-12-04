from collections import deque


def double(passwd):
    pairs = zip(passwd, passwd[1:])
    matches = [a == b for a, b in pairs]

    return any(matches)


def ascending(passwd):
    pairs = zip(passwd, passwd[1:])
    slopes = [a <= b for a, b in pairs]

    return all(slopes)


def only_double(passwd, pattern=None):
    if not passwd:
        return len(pattern) == 2

    nextup = deque([passwd.popleft()])

    if not pattern:
        return only_double(passwd, nextup)

    if pattern[0] == nextup[0]:
        return only_double(passwd, nextup + pattern)

    else:
        if len(pattern) == 2:
            return True
        else:
            return only_double(passwd, nextup)


def check(n, *checks):
    passwd = [int(d) for d in str(n)]

    return all(check(passwd) for check in checks)


def part1(start, end):
    return sum(check(num, double, ascending) for num in range(start, end))


def part2(start, end):
    return sum(
        check(num, ascending, lambda x: only_double(deque(x)))
        for num in range(start, end)
    )
