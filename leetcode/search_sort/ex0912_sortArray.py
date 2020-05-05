#! /usr/local/bin/python3
import random
from typing import List


def sortArray2(nums: List[int]) -> List[int]:
    return sorted(nums)


def sortArray(nums: List[int]) -> List[int]:
    length = len(nums)

    if length < 2:
        return nums

    # if length == 2:
    #    return nums if nums[0] <= nums[1] else [nums[1], nums[0]]

    pi = random.randint(0, length - 1)
    pivot = nums[pi]
    left = []
    right = []
    for i in range(length):
        if i != pi:
            if nums[i] < pivot:
                left.append(nums[i])
            else:
                right.append(nums[i])
    return sortArray(left) + [pivot] + sortArray(right)


def main():
    print(sortArray([5, 2, 3, 1]))
    print(sortArray([5, 1, 1, 2, 0, 0]))
    pass


if __name__ == "__main__":
    main()
