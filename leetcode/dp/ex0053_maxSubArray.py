#! /usr/local/bin/python3
from typing import List


def maxSubArray2(nums: List[int]) -> int:
    res = curr_max = -float('inf')  # res, curr_max represent total, current max value
    for i in nums:
        if curr_max < 0:            # curr_max is negative, only one number needs to be considered
            curr_max = max(curr_max, i)
        else:
            curr_max += i           # if curr_max turns to negative, next it will enter res < 0 branch
        res = max(res, curr_max)    # summary at last
    return res


def maxSubArray(nums: List[int]) -> int:
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]                             # dp[i] represent current sub array summary
    tmp = 0
    for i in range(1, n):
        if dp[i - 1] < 0:
            dp[i] = max(dp[i - 1], nums[i])
        elif nums[i] < 0:
            dp[i] = dp[i - 1]
            tmp += nums[i]                      # accumulate negative numbers
        else:
            dp[i] = max(dp[i - 1] + tmp + nums[i], nums[i])
            tmp = 0
    # print(dp)
    return max(dp)                              # return max sub array summary, not last one


def main():
    print(maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))     # 6
    print(maxSubArray([-2]))                                # -2
    print(maxSubArray([1, -1, 1]))                          # 1
    print(maxSubArray([8, -19, 5, -4, 20]))                 # 21


if __name__ == "__main__":
    main()
