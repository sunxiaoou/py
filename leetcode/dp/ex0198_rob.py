#! /usr/local/bin/python3
from typing import List


def rob(nums: List[int]) -> int:
    if not nums:
        return 0
    n = len(nums)
    if n == 1:
        return nums[0]
    dp = [0] * n
    for i in range(n):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])

    return dp[-1]


def main():
    print(rob([1, 2, 3, 1]))        # 4
    print(rob([2, 7, 9, 3, 1]))     # 12
    print(rob([0]))                 # 12


if __name__ == "__main__":
    main()
