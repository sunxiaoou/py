#! /usr/local/bin/python3
from typing import List


def maxSubArray(nums: List[int]) -> int:
    res = curr_max = -float('inf')  # res, curr_max represent total, current max value
    for i in nums:
        if curr_max < 0:            # curr_max is negative, only one number needs to be considered
            curr_max = max(curr_max, i)
        else:
            curr_max += i           # if curr_max turns to negative, next it will enter res < 0 branch
        res = max(res, curr_max)    # summary at last
    return res


def main():
    print(maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))     # 6
    print(maxSubArray([-2]))                                # -2
    print(maxSubArray([1, -1, 1]))                          # 1
    print(maxSubArray([8, -19, 5, -4, 20]))                 # 21


if __name__ == "__main__":
    main()
