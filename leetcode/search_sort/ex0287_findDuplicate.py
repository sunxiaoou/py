#! /usr/local/bin/python3
from typing import List


def findDuplicate_slow(nums: List[int]) -> int:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[j] == nums[i]:
                return nums[j]
    return -1


def findDuplicate(nums: List[int]) -> int:
    n = len(nums)
    le, ri = 1, n - 1       # bin search from 1 to n - 1 which is sorted, not unsorted nums[]
    ans = -1
    while le <= ri:
        mid = (le + ri) // 2
        # print(le, ri, mid)
        count = 0
        for i in range(n):
            if nums[i] <= mid:  # count how many numbers lees than mid
                count += 1
        if count <= mid:        # duplicate number is bigger than mid
            le = mid + 1
        else:                   # duplicate number is less than or equal mid
            ri = mid - 1
            ans = mid
        # print(le, ri)
    return ans


def main():
    print(findDuplicate([1, 3, 4, 2, 2]))       # 2
    print(findDuplicate([3, 1, 3, 4, 2]))       # 3


if __name__ == "__main__":
    main()
