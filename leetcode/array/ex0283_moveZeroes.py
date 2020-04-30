#! /usr/local/bin/python3
from typing import List


def moveZeroes_slow(nums: List[int]) -> None:
    def move(start, end):
        for i in range(start, end + 1):
            nums[i - 1] = nums[i]
        nums[end] = 0

    n = len(nums)
    nz = 0
    for i in range(n - 1, -1, -1):
        if nums[i] == 0:
            move(i + 1, n - 1 - nz)
            nz += 1


def moveZeroes(nums: List[int]) -> None:
    n = len(nums)
    last_non_zero_at = 0
    for i in range(n):
        if nums[i] != 0:
            nums[last_non_zero_at], nums[i] = nums[i], nums[last_non_zero_at]
            last_non_zero_at += 1


def main():
    nums = [0, 1, 0, 3, 12]
    # nums = [1, 2, 0]
    moveZeroes(nums)
    print(nums)


if __name__ == "__main__":
    main()
