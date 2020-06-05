#! /usr/local/bin/python3
from typing import List


def lengthOfLIS(nums: List[int]) -> int:
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    print(dp)
    return max(dp)


def main():
    print(lengthOfLIS([10, 9, 2, 5, 3, 7, 6, 39, 18]))  # 4
    # [1, 1, 1, 2, 2, 3, 3, 4, 4]
    print(lengthOfLIS([2, 1, 5, 0, 1, 2, 7, 2]))        # 4
    # [1, 1, 2, 1, 2, 3, 4, 3]


if __name__ == "__main__":
    main()
