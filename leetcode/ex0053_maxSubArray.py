#! /usr/local/bin/python3
from typing import List


def maxSubArray(nums: List[int]) -> int:
    n = len(nums)
    res = r2 = -float('inf')        # res, r2 represent current, history max value
    for i in range(n):
        if res < 0:                 # res is negative, only one number needs to be considered
            res = max(res, nums[i])
        else:
            res += nums[i]          # if res turns to negative, next it will enter res < 0 branch
        r2 = max(r2, res)
    return r2


def main():
    print(maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))     # 6
    print(maxSubArray([-2]))                                # -2
    print(maxSubArray([1, -1, 1]))                          # 1
    print(maxSubArray([8, -19, 5, -4, 20]))                 # 21


if __name__ == "__main__":
    main()
