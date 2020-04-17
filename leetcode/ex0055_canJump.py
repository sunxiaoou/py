#! /usr/local/bin/python3
from typing import List


def canJump_slow(nums: List[int]) -> bool:
    def backtrack(ans: List[int], left: int) -> bool:
        for i in range(nums[left], 0, -1):
            next = left + i
            if next >= len(nums) - 1:
                # print(ans)
                return True
            if nums[next] > 0:
                ans.append(next)
                print(ans)
                if backtrack(ans, next) is True:
                    return True
                print(ans)
                ans.pop()
        else:
            return False
    return backtrack([], 0)


def canJump(nums: List[int]) -> bool:
    j = 0
    can = True
    for i in range(len(nums) - 2, -1, -1):
        if can and not nums[i]:                     # only zero can block jump
            can = False
            j = i
        elif can is False and nums[i] > j - i:      # can previous num skip gaps?
            can = True
            j = 0
    return can


def main():
    print(canJump([2, 3, 1, 2, 4]))
    print(canJump(([3, 2, 1, 0, 4])))

    #       0  1  2  3  4  5  6  7  8  9
    nums = [2, 0, 6, 9, 8, 4, 5, 0, 8, 9,   # 0
            1, 2, 9, 6, 8, 8, 0, 6, 3, 1,   # 1
            2, 2, 1, 2, 6, 5, 3, 1, 2, 2,   # 2
            6, 4, 2, 4, 3, 0, 0, 0, 3, 8,   # 3
            2, 4, 0, 1, 2, 0, 1, 4, 6, 5,   # 4
            8, 0, 7, 9, 3, 4, 6, 6, 5, 8,   # 5
            9, 3, 4, 3, 7, 0, 4, 9, 0, 9,   # 6
            8, 4, 3, 0, 7, 7, 1, 9, 1, 9,   # 7
            4, 9, 0, 1, 9, 5, 7, 7, 1, 5,   # 8
            8, 2, 8, 2, 6, 8, 2, 2, 7, 5,   # 9
            1, 7, 9, 6]
    print(canJump(nums))


if __name__ == "__main__":
    main()
