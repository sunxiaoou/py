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


def trap2(height: List[int]) -> int:
    if not height:
        return 0

    maximum = max(height)
    i = height.index(maximum)
    water = trap1(height[: i + 1])

    h2 = height[i:]
    h2 = h2[::-1]
    water += trap1(h2)
    return water


# Monotone Stack
def trap(height: List[int]) -> int:
    n = len(height)
    stack = []
    res = i = 0
    while i < n:
        if not stack or height[stack[-1]] > height[i]:  # Monotone decreasing stack
            stack.append(i)
            i += 1
        else:                                   # i is right border
            bottom = height[stack.pop()]        # firstly, stack[-1] is bottom
            if stack:                           # then stack[-1] is left border
                res += (min(height[stack[-1]], height[i]) - bottom) * (i - stack[-1] - 1)
    return res


def main():
    print(trap([4, 2, 3]))                              # 1
    #           0  1  2  3  4  5  6  7  8  9 10 11
    print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # 6
    print(trap([]))                                     # 0
    print(trap([1]))                                    # 0


if __name__ == "__main__":
    main()
