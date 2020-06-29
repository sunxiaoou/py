#! /usr/local/bin/python3
from typing import List


# double pointers
def minSubArrayLen(s: int, nums: List[int]) -> int:
    n = len(nums)
    i = j = cs = 0                  # cs is current sum(i...j)
    mini = float('inf')
    while j < n:
        while cs < s and j < n:
            cs += nums[j]
            j += 1
        if cs < s:                  # cs < s and j == n
            break
        while cs - nums[i] >= s:
            cs -= nums[i]
            i += 1
        mini = min(mini, j - i)
        # print(cs, mini)
        cs -= nums[i]
        i += 1
    return 0 if mini == float('inf') else mini


def main():
    print(minSubArrayLen(7, [1, 2]))                # 0
    print(minSubArrayLen(7, []))                    # 0
    print(minSubArrayLen(7, [8]))                   # 1
    print(minSubArrayLen(7, [2, 3, 1, 2, 4, 3]))    # 2
    pass


if __name__ == "__main__":
    main()
