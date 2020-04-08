#! /usr/local/bin/python3
from typing import List


# https://leetcode-cn.com/problems/two-sum/
def twoSum_slow(nums: List[int], target: int) -> List[int]:
    for i in range(0, target // 2 + 1):
        if i in nums and target - i in nums:
            if i != target - i:
                return [nums.index(i), nums.index(target - i)]
            first = nums.index(i)
            try:
                second = nums[first + 1:].index(i) + first + 1
            except ValueError:
                pass
            else:
                return [first, second]
    i = -1
    while True:
        if i in nums and target - i in nums:
            if i != target - i:
                return [nums.index(i), nums.index(target - i)]
            first = nums.index(i)
            try:
                second = nums[first + 1:].index(i) + first + 1
            except ValueError:
                pass
            else:
                return [first, second]
        i -= 1


def twoSum(nums: List[int], target: int) -> List[int]:
    dictionary = {}
    for i, n in enumerate(nums):
        if target - n in dictionary:
            return [dictionary[target - n], i]
        dictionary[n] = i


def main():
    print(twoSum([2, 7, 11, 15], 9))    # [0, 1]
    print(twoSum([2, 3, 3, 11, 15], 6))    # [1, 2]
    # print(twoSum([2, 3, 11, 15], 6))    # [0, 1]
    print(twoSum([0, 4, 3, 0], 0))    # [0, 3]
    print(twoSum([0, -4, 3, 0], -1))    # [1, 2]
    print(twoSum([-1, -4, 3, -1], -2))    # [0, 3]
    print(twoSum([-3, 4, 3, 90], 0))    # [0, 2]


if __name__ == "__main__":
    main()
