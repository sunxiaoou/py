#! /usr/local/bin/python3
from typing import List


def searchRange(nums: List[int], target: int) -> List[int]:
    n = len(nums)
    le, ri = 0, n - 1
    while le <= ri:
        mid = (le + ri) // 2
        if nums[mid] == target:
            le = mid - 1
            while le >= 0 and nums[le] == target:
                le -= 1
            ri = mid + 1
            while ri < n and nums[ri] == target:
                ri += 1
            return [le + 1, ri - 1]
        if nums[mid] < target:
            le = mid + 1
        else:
            ri = mid - 1
    return [-1, -1]


def main():
    print(searchRange([1, 5], 5))               # [1, 1]
    print(searchRange([5, 5, 5, 5, 5, 5], 5))   # [0, 5]
    print(searchRange([5,7,7,8,8,10], 8))       # [3, 4]
    print(searchRange([5,7,7,8,8,10], 6))       # [-1, -1]


if __name__ == "__main__":
    main()
