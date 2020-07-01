#! /usr/local/bin/python3
from typing import List


def largestRectangleArea_slow(heights: List[int]) -> int:
    n = len(heights)
    res = 0
    for i in range(n):
        j = i - 1
        area = heights[i]
        while j > -1 and heights[j] >= heights[i]:
            area += heights[i]
            j -= 1
        j = i + 1
        while j < n and heights[j] >= heights[i]:
            area += heights[i]
            j += 1
        res = max(res, area)
    return res


# monotone increasing stack
def largestRectangleArea(heights: List[int]) -> int:
    heights = [0] + heights + [0]       # add 2 sentinels
    n = len(heights)
    stack = [0]                         # push first sentinel
    res = 0
    for i in range(1, n):
        while heights[stack[-1]] > heights[i]:
            j = stack.pop()
            area = heights[j] * (i - stack[-1] - 1)
            print([heights[x] for x in stack], "-", area)
            res = max(res, area)
        stack.append(i)
        print([heights[x] for x in stack])
    return res


def main():
    print(largestRectangleArea([2, 2, 5, 6, 2, 3]))     # 12
    """
    [0, 2]                  # push 2
    [0, 2, 2]               # push 2
    [0, 2, 2, 5]            # push 5
    [0, 2, 2, 5, 6]         # push 6
    [0, 2, 2, 5] - 6        # pop 6, calculate area 6 
    [0, 2, 2] - 10          # pop 6, calculate area 10
    [0, 2, 2, 2]            # push 2
    [0, 2, 2, 2, 3]         # push 3
    [0, 2, 2, 2] - 3        # pop 3, calculate area 3
    [0, 2, 2] - 8           # pop 2, calculate area 8
    [0, 2] - 10             # pop 2, calculate area 10
    [0] - 12                # pop 2, calculate area 12
    [0, 0]
    """
    print(largestRectangleArea([2, 1, 5, 6, 2, 3]))     # 10
    print(largestRectangleArea([]))                     # 0


if __name__ == "__main__":
    main()
