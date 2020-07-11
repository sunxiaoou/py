#! /usr/local/bin/python3
from typing import List


def majorityElement(nums: List[int]) -> int:
    n = len(nums)
    for i in set(nums):
        if nums.count(i) > n // 2:
            return i


def main():
    print(majorityElement([3, 2, 3]))                       # 3
    print(majorityElement([2, 2, 1, 1, 1, 2, 2]))           # 2


if __name__ == "__main__":
    main()
