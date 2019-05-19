#! /usr/local/bin/python3

from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    length = len(nums)
    if length == 2:
        if nums[0] + nums[1] == target:
            return nums
        else:
            return []

    for i in nums[1:]:
        result = two_sum([nums[0], i], target)
        if result:
            return result
    return two_sum(nums[1:], target)


def twoSum(nums: List[int], target: int) -> List[int]:
    values = two_sum(nums, target)
    i0 = nums.index(values[0])
    if values[0] == values[1]:
        nums[i0] = values[0] + 1
    i1 = nums.index(values[1])
    return [i0, i1]


def main():
    # nums = [2, 7, 11, 15, 17]
    nums = [1, 2, 3, 2, 3]
    print(twoSum(nums, 6))


if __name__ == "__main__":
    main()
