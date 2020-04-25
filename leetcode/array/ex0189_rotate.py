#! /usr/local/bin/python3
from typing import List


def rotate_slow(nums: List[int], k: int) -> None:
    for _ in range(k):
        i, x = 0, nums[0]
        for _ in nums:
            j = (i + 1) % len(nums)
            x, nums[j] = nums[j], x
            i = j
    print(nums)


"""
rotate via 3 reverses, for example n = 7, k = 3
original nums:          [1, 2, 3, 4, 5, 6, 7]
reverse nums:           [7, 6, 5, 4, 3, 2, 1]
reverse nums[: k]       [5, 6, 7, 4, 3, 2, 1]
reverse nums[k:]        [5, 6, 7, 1, 2, 3, 4]
but we cannot use slices like nums[: k] here, since it doesn't change origin nums
"""


def rotate2(nums: List[int], k: int) -> None:
    n = len(nums)
    k %= n          # to avoid index error

    for i in range(n // 2):
        nums[i], nums[n - 1 - i] = nums[n - 1 - i], nums[i]

    for i in range(k // 2):
        nums[i], nums[k - 1 - i] = nums[k - 1 - i], nums[i]

    for i in range((n - k) // 2):
        nums[i + k], nums[n - 1 - i] = nums[n - 1 - i], nums[i + k]


def rotate(nums: List[int], k: int) -> None:
    n = len(nums)
    k %= n

    def reverse(left: int, right: int):
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)


def test(nums: List[int], k: int):
    rotate(nums, k)
    print(nums)


def main():
    test([1], 2)                      # [1]
    test([1, 2], 3)                   # [2, 1]
    test([1, 2, 3, 4, 5, 6, 7], 3)    # [5, 6, 7, 1, 2, 3, 4]
    test([-1, -100, 3, 99], 2)        # [3, 99, -1, -100]


if __name__ == "__main__":
    main()
