#! /usr/local/bin/python3
from typing import List


def missingNumber(nums: List[int]) -> int:
    print(nums)
    length = len(nums)
    left = 0
    right = length - 1
    while left <= right:
        mid = (left + right) // 2
        # print("-", left, mid, right)
        if nums[mid] != mid:
            right = mid - 1
        else:
            left = mid + 1
    print(':', left, right)
    return left


def main():
    print(missingNumber([0, 1, 3]))
    print(missingNumber([0, 1, 2, 3, 4, 5, 6, 7, 9]))
    print(missingNumber([0, 1, 3, 4, 5, 6, 7]))
    print(missingNumber([0, 2, 3, 4, 5, 6, 7, 8]))
    print(missingNumber([0, 2, 3, 4, 5, 6, 7]))
    print(missingNumber([1, 2, 3, 4, 5, 6, 7]))
    print(missingNumber([0]))
    print(missingNumber([1]))
    print(missingNumber([1, 2]))
    print(missingNumber([0, 1]))


if __name__ == "__main__":
    main()
