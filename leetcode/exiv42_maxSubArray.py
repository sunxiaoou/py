#! /usr/local/bin/python3
from typing import List


def maxSubArray(nums: List[int]) -> int:
    if all(n < 0 for n in nums):
        return max(n for n in nums)

    summary = maximum = 0
    for n in nums:
        summary += n
        if summary < 0:
            summary = 0
        elif summary > maximum:
            maximum = summary
    return maximum


def maxSubArray2(nums: List[int]) -> int:
    summary = 0
    maximum = nums[0]
    for n in nums:
        if summary <= 0:
            summary = n
        else:
            summary += n
        maximum = max(maximum, summary)
    return maximum


def main():
    print(maxSubArray2([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
    print(maxSubArray2([-2, -1]))
    print(maxSubArray2([1, -1, 1]))
    print(maxSubArray2([1, -1, -2]))
    print(maxSubArray2([-1]))


if __name__ == "__main__":
    main()
