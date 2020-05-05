#! /usr/local/bin/python3
from typing import List


def merge(nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    for i in range(m, m + n):
        nums1[i] = None
    # print(nums1)

    i = 0
    for a in nums2:
        while nums1[i] is not None and nums1[i] <= a:
            i += 1
        for j in range(m + n - 1, i, -1):
            nums1[j] = nums1[j - 1]
        nums1[i] = a
        i += 1


def test(nums1: List[int], m: int, nums2: List[int], n: int) -> List[int]:
    merge(nums1, m, nums2, n)
    return nums1


def main():
    print(test([-1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0], 5, [-1, -1, 0, 0, 1, 2], 6))
    # [-1, -1, -1, 0, 0, 0, 0, 0, 1, 2, 3]
    print(test([-1, 0, 0, 3, 3, 3, 0, 0, 0], 6, [1, 2, 2], 3))  # [-1, 0, 0, 1, 2, 2, 3, 3, 3]
    print(test([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3))            # [1, 2, 2, 3, 5, 6]


if __name__ == "__main__":
    main()
