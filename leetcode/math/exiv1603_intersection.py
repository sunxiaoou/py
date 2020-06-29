#! /usr/local/bin/python3
from typing import List


def is_horizontal(start: List[int], end: List[int]):
    return True if start[1] == end[1] else False


def is_vertical(start: List[int], end: List[int]):
    return True if start[0] == end[0] else False


def is_in(c: float, a: int, b: int) -> bool:
    return a <= c <= b or a >= c >= b


# y = x * a + b     # a is slope, b is y_intercept
def get_equation(start: List[int], end: List[int]) -> List[float]:
    x1, y1 = start
    x2, y2 = end
    slope = (y1 - y2) / (x1 - x2)
    y_intercept = y1 - x1 * (y1 - y2) / (x1 - x2)
    return [slope, y_intercept]


# convert lines to equations and solve
def intersection(start1: List[int], end1: List[int], start2: List[int], end2: List[int]) -> List[float]:
    if is_horizontal(start1, end1) and is_vertical(start2, end2):
        x, y = start2[0], start1[1]
        if is_in(x, start1[0], end1[0]) and is_in(y, start2[1], end2[1]):
            return [x, y]
        return []
    if is_vertical(start1, end1) and is_horizontal(start2, end2):
        return intersection(start2, end2, start1, end1)         # exchange line segment 1 and 2
    if is_vertical(start1, end1) or is_vertical(start2, end2):
        # exchange x, y to avoid divide zero in vertical line
        return intersection(start1[:: -1], end1[:: -1], start2[:: -1], end2[:: -1])[:: -1]

    a1, b1 = get_equation(start1, end1)
    a2, b2 = get_equation(start2, end2)
    # print(a1, b1, a2, b2)
    if a1 == a2 and b1 == b2:       # two segments on same line
        x, y = sorted([start1, end1, start2, end2])[1]
        if is_in(x, start1[0], end1[0]) and is_in(x, start2[0], end2[0]):
            return [x, y]           # there is overlap
        return []
    if a1 == a2 or b1 == b2:        # two segments are parallel
        return []
    x = (b2 - b1) / (a1 - a2)       # x * a1 + b1 == y == x * a2 + b2
    y = a1 * (b2 - b1) / (a1 - a2) + b1         # y = a1 * x + b1
    if is_in(x, start1[0], end1[0]) and is_in(x, start2[0], end2[0]):
        return [x, y]
    return []


def main():
    print(intersection([0, 0], [0, 1], [0, 2], [0, 3]))         # []
    print(intersection([0, 0], [2, 1], [1, 0], [1, 3]))         # [1.0, 0.5]
    print(intersection([1, 0], [1, 3], [0, 0], [2, 1]))         # [1.0, 0.5]
    print(intersection([1, 2], [4, 2], [3, 0], [3, 5]))         # [3, 2]
    print(intersection([3, 0], [3, 5], [1, 2], [4, 2]))         # [3, 2]
    print(intersection([0, 0], [1, 0], [1, 1], [0, -1]))        # [0.5, 0.0]
    print(intersection([0, 0], [3, 3], [1, 1], [2, 2]))         # [1, 1]
    print(intersection([0, 0], [1, 1], [1, 0], [2, 1]))         # []
    print(intersection([0, 0], [0, 1], [1, 0], [1, 1]))         # []


if __name__ == "__main__":
    main()
