#! /usr/local/bin/python3
import random
from typing import List


def findKthLargest2(nums: List[int], k: int) -> int:
    return sorted(nums, reverse=True)[k - 1]


def sort_reverse(nums: List[int]) -> List[int]:
    n = len(nums)
    if n < 2 or n == nums.count(nums[0]):
        return nums
    pivot = random.choice(nums)
    left, right = [], []
    for i in nums:
        if i > pivot:
            left.append(i)
        else:
            right.append(i)
    return sort_reverse(left) + sort_reverse(right)


def findKthLargest(nums: List[int], k: int) -> int:
    return sort_reverse(nums)[k - 1]


def main():
    print(findKthLargest([3, 2, 1, 5, 6, 4], 2))            # 5
    print(findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))   # 4


if __name__ == "__main__":
    main()
