#! /usr/local/bin/python3
from typing import List


def search(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:                # use >= instead of >, as left == right is OK
        mid = (left + right) // 2
        if target == nums[mid]:
            return mid
        if target > nums[mid] > nums[left] or nums[right] >= target > nums[mid] or\
                nums[mid] > nums[right] >= target:
            left = mid + 1              # use mid + 1 instead of mid to avoid infinite loop
        elif target < nums[mid] < nums[right] or nums[left] <= target < nums[mid] or\
                nums[mid] < nums[left] <= target:
            right = mid - 1             # use mid - 1 instead of mid to avoid infinite loop
        else:
            # print(left, right, mid)
            break
    return -1


def main():
    print(search([5, 1, 2], 5))         # 0
    print(search([4, 5, 6, 7, 0, 1, 2], 4))         # 0
    print(search([4, 5, 6, 7, 0, 1, 2], 5))         # 1
    print(search([4, 5, 6, 7, 0, 1, 2], 6))         # 2
    print(search([4, 5, 6, 7, 0, 1, 2], 7))         # 3
    print(search([4, 5, 6, 7, 0, 1, 2], 0))         # 4
    print(search([4, 5, 6, 7, 0, 1, 2], 1))         # 5
    print(search([4, 5, 6, 7, 0, 1, 2], 2))         # 6
    print(search([4, 5, 6, 7, 0, 1, 2], 3))         # -1


if __name__ == "__main__":
    main()
