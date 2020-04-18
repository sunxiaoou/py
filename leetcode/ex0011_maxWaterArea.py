#! /usr/local/bin/python3
from typing import List


def maxArea_slow(height: List[int]) -> int:
    n = len(height)
    points = [i for i in enumerate(height)]
    # print(points)
    res = 0
    for i in range(n):
        for j in range(i + 1, n):
            area = (points[j][0] - points[i][0]) * min(points[j][1], points[i][1])
            res = max(res, area)
    return res


"""
input [1, 3, 4, 2, 1, 1]

        __|                     # actually we need to find 3 rectangles which 
       |__|__                   # area are 1 * 5, 3 * 1 and 2 * 2 respectively
     __|__|__|_____             # from left to right, find 1 * 5 and 3 * 1
    |__|__|__|__|__|            # from right to left, find 2 * 2
    0  1  2  3  4  5

"""

def maxArea(height: List[int]) -> int:
    n = len(height)
    area = 0
    for i in range(n - 1):
        if i == 0 or height[left] < height[i]:
            left = i
            for j in range(n - 1, left, -1):
                if height[j] >= height[left]:
                    break
            area = max(area, min(height[j], height[left]) * (j - left))
            # print(left, height[left], area)

    right = n - 1
    for i in range(n - 1, 0, -1):
        if height[right] < height[i]:
            for j in range(right):
                if height[j] >= height[right]:
                    break
            area = max(area, min(height[right], height[j]) * (right - j))
            # print(right, height[right], area)
            right = i
    return area


def main():
    print(maxArea([1, 1]))                          # 1
    print(maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))     # 49
    # print(maxArea_slow([1, 2, 4, 3]))     # 4
    print(maxArea([1, 2, 4, 3]))                    # 4
    # print(maxArea_slow([1, 3, 4, 2, 1, 1]))     # 5
    print(maxArea([1, 3, 4, 2, 1, 1]))              # 5
    print(maxArea([10, 14, 10, 4, 10, 2, 6, 1, 6, 12]))     # 96


if __name__ == "__main__":
    main()
