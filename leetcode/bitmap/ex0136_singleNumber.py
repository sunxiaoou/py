#! /usr/local/bin/python3
from typing import List


def singleNumber_slow(nums: List[int]) -> int:
    nums.sort()
    i, j = 0, 0
    for j in range(1, len(nums)):
        if nums[j] > nums[i]:
            if i + 1 == j:
                return nums[i]
            i = j
    if i == j:
        return nums[i]


def singleNumber(nums: List[int]) -> int:
    x = 0
    for i in nums:
        x ^= i
    return x


def main():
    print(singleNumber([2, 2, 1]))          # 1
    print(singleNumber([4, 1, 2, 1, 2]))    # 4


if __name__ == "__main__":
    main()
