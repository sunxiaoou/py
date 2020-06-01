#! /usr/local/bin/python3
from typing import List


def findPeakElement(nums: List[int]) -> int:
    i, peak = 0, nums[0]
    for i in range(1, len(nums)):
        if peak > nums[i]:
            return i - 1
        else:
            peak = nums[i]
    return i


def main():
    print(findPeakElement([1]))                     # 0
    print(findPeakElement([1, 2, 3, 1]))            # 2
    print(findPeakElement([1, 2, 1, 3, 5, 6, 4]))   # 1 or 5


if __name__ == "__main__":
    main()
