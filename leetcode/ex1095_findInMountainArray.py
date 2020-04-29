#! /usr/local/bin/python3
from typing import List


class MountainArray:
    def __init__(self, nums: List[int]):
        self.nums = nums

    def get(self, index: int) -> int:
        return self.nums[index]

    def length(self) -> int:
        return len(self.nums)


def findInMountainArray2(nums: List[int], target: int) -> int:
    n = len(nums)
    left, right = 0, n - 1
    while left < right:
        mid = (left + right) // 2
        if (mid > 0 and nums[mid] > nums[mid - 1]) or (mid == 0 and nums[mid] < nums[mid + 1]):
            if nums[mid] > nums[mid + 1]:               # is it peak?
                left = mid
                break
            left = mid + 1
        else:
            right = mid - 1
    peak = left
    # print(peak)

    def binary_search(left: int, right: int, ascending: bool=True) -> int:
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif (ascending and nums[mid] < target) or (not ascending and nums[mid] > target):
                left = mid + 1
            else:
                right = mid - 1
        return -1

    index = binary_search(0, peak)
    if index >= 0:
        return index

    return binary_search(peak + 1, n - 1, False)


def findInMountainArray(target: int, mountain_arr: 'MountainArray') -> int:
    n = mountain_arr.length()
    left, right = 0, n - 1
    while left < right:
        mid = (left + right) // 2
        if (mid > 0 and mountain_arr.get(mid) > mountain_arr.get(mid - 1)) or \
                (mid == 0 and mountain_arr.get(mid) < mountain_arr.get(mid + 1)):
            if mountain_arr.get(mid) > mountain_arr.get(mid + 1):
                left = mid
                break
            left = mid + 1
        else:
            right = mid - 1
    peak = left
    # print(peak)

    def binary_search(left: int, right: int, ascending: bool=True) -> int:
        while left <= right:
            mid = (left + right) // 2
            if mountain_arr.get(mid) == target:
                return mid
            elif (ascending and mountain_arr.get(mid) < target) or (not ascending and mountain_arr.get(mid) > target):
                left = mid + 1
            else:
                right = mid - 1
        return -1

    index = binary_search(0, peak)
    if index >= 0:
        return index

    return binary_search(peak + 1, n - 1, False)


def main():
    print(findInMountainArray2([1, 5, 2], 1))                               # 0
    print(findInMountainArray(1, MountainArray([1, 5, 2])))                 # 0
    print(findInMountainArray2([1, 2, 3, 4, 5, 3, 1], 3))                   # 2
    print(findInMountainArray(3, MountainArray([1, 2, 3, 4, 5, 3, 1])))     # 2
    print(findInMountainArray2([0, 1, 2, 4, 2, 1], 3))                      # -1
    print(findInMountainArray(3, MountainArray([0, 1, 2, 4, 2, 1])))        # -1
    print(findInMountainArray2([0, 4, 3, 2, 1], 1))                         # 4
    print(findInMountainArray(1, MountainArray([0, 4, 3, 2, 1])))           # 4


if __name__ == "__main__":
    main()
