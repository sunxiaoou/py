#! /usr/local/bin/python3
from typing import List


def sortColors(nums: List[int]) -> None:
    n = len(nums)
    c0 = c1 = 0
    for i in nums:
        if i == 0:
            c0 += 1
        elif i == 1:
            c1 += 1
    for i in range(n):
        if i < c0:
            nums[i] = 0
        elif i < c0 + c1:
            nums[i] = 1
        else:
            nums[i] = 2


def main():
    # nums = [2, 0, 2, 1, 1, 0]
    nums = [1]
    sortColors(nums)
    print(nums)     # [0, 0, 1, 1, 2, 2]


if __name__ == "__main__":
    main()
