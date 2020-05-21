#! /usr/local/bin/python3
from typing import List


def maxProduct(nums: List[int]) -> int:
    n = len(nums)
    dp = [0] * n        # dp_min, we need this because dp_max depends on it
    dp2 = [0] * n       # dp_max，vice versa
    dp[0] = dp2[0] = nums[0]
    for i in range(1, n):
        if nums[i] < 0:
            dp[i] = min(dp2[i - 1] * nums[i], nums[i])
            dp2[i] = max(dp[i - 1] * nums[i], nums[i])
        else:
            dp[i] = min(dp[i - 1] * nums[i], nums[i])
            dp2[i] = max(dp2[i - 1] * nums[i], nums[i])
    # print(dp)
    # print(dp2)
    return max(dp2)


def main():
    print(maxProduct([2, -5, -2, -4, 3]))   # 24
    print(maxProduct([3, -2, 4]))           # 4
    print(maxProduct([-2, 4, -1]))          # 8
    print(maxProduct([0, 2]))               # 2
    print(maxProduct([2, 3, -2, 4]))        # 6
    print(maxProduct([-2, 0, -1]))          # 0


if __name__ == "__main__":
    main()
