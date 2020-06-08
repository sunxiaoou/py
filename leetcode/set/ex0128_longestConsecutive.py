#! /usr/local/bin/python3
from typing import List


# this may leads to memory error
def longestConsecutive_err(nums: List[int]) -> int:
    if not nums:
        return 0
    mini = min(nums)
    leng = max(nums) - mini + 1
    flags = [0] * leng
    for i in nums:
        flags[i - mini] = 1

    res = count = 0
    for i in flags:
        if i:
            count += 1
            res = max(res, count)
        else:
            count = 0
    return res


def longestConsecutive(nums: List[int]) -> int:
    nset = set(nums)
    res = 0
    for i in nset:
        if i - 1 not in nset:
            count, j = 1, i
            while j + 1 in nset:
                count += 1
                j += 1
            res = max(res, count)
    return res


def main():
    print(longestConsecutive([100, 4, 200, 1, 3, 2]))       # 4
    print(longestConsecutive([0]))                          # 1
    print(longestConsecutive([2147483646, -2147483647, 0, 2, 2147483644,  2147483645]))     # 3


if __name__ == "__main__":
    main()
