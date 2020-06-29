#! /usr/local/bin/python3
from typing import List


# local hash algorithm
def firstMissingPositive(nums: List[int]) -> int:
    n = len(nums)
    for i in range(n):
        if nums[i] < 1:         # illegal value
            nums[i] = n + 1     # set to n + 1 to avoid negative "mark"
    # print(nums)
    for i in range(n):
        if abs(nums[i]) < n + 1:        # legal value
            ind = abs(nums[i]) - 1      # get corresponding index
            nums[ind] = -(abs(nums[ind]))   # turn value in the index to negative as a mark
    # print(nums)
    for i in range(n):
        if nums[i] > 0:         # this index is not marked as negative,
            return i + 1        # it means the corresponding num is meaning
    return n + 1                # all indexes are marked to negative


def main():
    print(firstMissingPositive([3, 4, -1, 1]))      # 2
    print(firstMissingPositive([1, 2, 2]))          # 3
    print(firstMissingPositive([7, 8, 9, 11, 12]))  # 1
    print(firstMissingPositive([2, 3, 1]))          # 4


if __name__ == "__main__":
    main()
