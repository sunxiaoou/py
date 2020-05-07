#! /usr/local/bin/python3
from typing import List


def jump(nums: List[int]) -> int:
    steps = curr_reach = next_reach = 0
    for i in range(len(nums)):
        if curr_reach < i:
            curr_reach = next_reach
            steps += 1
        next_reach = max(next_reach, i + nums[i])
    if curr_reach < len(nums) - 1:
        return -1
    return steps


def main():
    print(jump([10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 0]))      # 2
    print(jump([1, 1, 1, 1]))                               # 3
    print(jump([2, 3, 1, 1, 4]))                            # 2
    print(jump([0]))                                        # 0
    print(jump([2, 0, 1]))                                  # 1
    print(jump([2, 0, 1, 1]))                               # 2
    print(jump([2, 0, 0, 1]))                               # 2


if __name__ == "__main__":
    main()
