#! /usr/local/bin/python3
from typing import List


def threeSumClosest(nums: List[int], target: int) -> int:
    nums.sort()
    n = len(nums)
    ans = float('inf')
    for i in range(n):
        le, ri = i + 1, n - 1
        while le < ri:
            s = nums[i] + nums[le] + nums[ri]
            # print(nums[i], nums[le], nums[ri], s)
            if s == target:
                return s
            if abs(s - target) < abs(ans - target):
                ans = s
            if s < target:
                le += 1
            else:
                ri -= 1
    return ans


def main():
    print(threeSumClosest([-1, 2, 1, -4], 1))      # 2


if __name__ == "__main__":
    main()
