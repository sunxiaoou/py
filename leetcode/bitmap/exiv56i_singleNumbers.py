#! /usr/local/bin/python3
from typing import List


def singleNumbers2(nums: List[int]) -> List[int]:
    dictionary = {}
    for i in nums:
        if i in dictionary:
            dictionary.pop(i)
        else:
            dictionary[i] = 0
    return list(dictionary.keys())


# https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-lcof/solution/
# shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-by-leetcode/
def singleNumbers(nums: List[int]) -> List[int]:
    xor = 0                 # get xor of 2 single numbers
    for i in nums:
        xor ^= i

    a = 1                   # get first non zero bit in xor
    while xor & a == 0:
        a <<= 1

    x, y = 0, 0          # split to 2 groups, xor respectively
    for i in nums:
        if i & a == 0:
            x ^= i
        else:
            y ^= i
    return [x, y]        # result is the single numbers


def main():
    print(singleNumbers([4, 1, 4, 6]))                  # [1, 6] or [6, 1]
    print(singleNumbers([1, 2, 10, 4, 1, 4, 3, 3]))     # [2, 10] or [10, 2]


if __name__ == "__main__":
    main()
