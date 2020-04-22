#! /usr/local/bin/python3
from typing import List


def removeDuplicates_slow(nums: List[int]) -> int:
    i, j = 0, 1
    while j < len(nums):
        if nums[i] < nums[j]:
            if j == i + 1:
                i += 1
                j += 1
            else:
                nums[i + 1:] = nums[j: len(nums)]
                i += 1
                j = i + 1
        elif j + 1 == len(nums):
            return i + 1
        else:
            j += 1
    return j


def removeDuplicates(nums: List[int]) -> int:
    i = 0
    for j in range(1, len(nums)):
        if nums[j] > nums[i]:
            i += 1
            nums[i] = nums[j]
    return i + 1


def test(nums: List[int]):
    n = removeDuplicates(nums)
    print(nums[: n])


def main():
    test([1, 1])                            # [1]
    test([1, 1, 2])                         # [1, 2]
    test([0, 0, 1, 1, 1, 2, 2, 3, 3, 4])    # [0, 1, 2, 3, 4]


if __name__ == "__main__":
    main()
