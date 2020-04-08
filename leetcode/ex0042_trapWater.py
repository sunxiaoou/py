#! /usr/local/bin/python3
from typing import List


def trap1(height: List[int]) -> int:
    begin = 0
    water = 0
    for i in range(1, len(height)):
        if height[i] >= height[begin]:
            for he in height[begin + 1: i]:
                water += height[begin] - he
            begin = i
            # print(begin, water, end=', ')
    # print()
    return water


def trap(height: List[int]) -> int:
    if not height:
        return 0

    maximum = max(height)
    i = height.index(maximum)
    water = trap1(height[: i + 1])

    h2 = height[i:]
    h2 = h2[::-1]
    water += trap1(h2)
    return water


def main():
    # print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
    print(trap([]))
    print(trap([1]))


if __name__ == "__main__":
    main()
