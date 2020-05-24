#! /usr/local/bin/python3
from bisect import insort
from typing import List


def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    m, n = len(nums1), len(nums2)
    if m < n:
        return findMedianSortedArrays(nums2, nums1)
    for i in nums2:
        insort(nums1, i)
    print(nums1)
    qu, re = divmod(m + n, 2)
    if re:
        return float(nums1[qu])
    return (nums1[qu - 1] + nums1[qu]) / 2


def main():
    print(findMedianSortedArrays([1, 2], [1, 2, 3]))    # 2.0
    return
    print(findMedianSortedArrays([1, 3], [2]))          # 2.0
    print(findMedianSortedArrays([1, 2], [3, 4]))       # 2.5


if __name__ == "__main__":
    main()
