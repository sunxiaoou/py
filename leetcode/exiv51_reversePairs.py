#! /usr/local/bin/python3
# https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/
# solution/shu-zu-zhong-de-ni-xu-dui-by-leetcode-solution/

from random import shuffle
from typing import List


def reversePairs(nums: List[int]) -> int:
    n = len(nums)
    if n < 2:
        return 0

    res = [0] * n
    count = 0

    def merge_sort(left: int, right: int):
        nonlocal count
        if left == right:
            return
        mid = (left + right) // 2
        merge_sort(left, mid)
        merge_sort(mid + 1, right)
        i, j, k = left, mid + 1, left
        while k <= right:
            if i <= mid and (j > right or nums[i] <= nums[j]):
                res[k] = nums[i]
                i += 1
                count += j - mid - 1
            elif j <= right and (i > mid or nums[i] > nums[j]):
                res[k] = nums[j]
                j += 1
            k += 1
        for i in range(left, right + 1):
            nums[i] = res[i]
        # print(left, right, nums)

    merge_sort(0, n - 1)
    # print(nums)
    return count


def main():
    print(reversePairs([]))
    print(reversePairs([1, 3, 2, 3, 1]))

    nums = [i for i in range(10)]
    shuffle(nums)
    # print(nums)
    print(reversePairs(nums))

    print(reversePairs([4, 5, 6, 7]))         # 0
    print(reversePairs([7, 5]))             # 1
    print(reversePairs([7, 5, 6, 4]))       # 5


if __name__ == "__main__":
    main()
