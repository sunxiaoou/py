#! /usr/local/bin/python3
from typing import List


def intersect(nums1: List[int], nums2: List[int]) -> List[int]:
    nums1.sort()
    nums2.sort()
    n1, n2 = len(nums1), len(nums2)
    i, j, res = 0, 0, []
    while i < n1 and j < n2:
        if nums1[i] == nums2[j]:
            res.append(nums1[i])
            i += 1
            j += 1
        elif nums1[i] < nums2[j]:
            i += 1
        else:
            j += 1
    return res


def main():
    print(intersect([1, 2, 2, 1], [2, 2]))          # [2, 2]
    print(intersect([4, 9, 5], [9, 4, 9, 8, 4]))    # [4, 9]
    pass


if __name__ == "__main__":
    main()
