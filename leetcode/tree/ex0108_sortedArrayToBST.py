#! /usr/local/bin/python3
from typing import List

from treeNode import TreeNode


def sortedArrayToBST(nums: List[int]) -> TreeNode:
    if not nums:
        return None
    n = len(nums)
    mid = n // 2
    root = TreeNode(nums[mid])
    if mid > 0:
        root.left = sortedArrayToBST(nums[: mid])
    if mid < n - 1:
        root.right = sortedArrayToBST(nums[mid + 1:])
    return root


def main():
    print(sortedArrayToBST([-10, -3, 0, 5, 9]).show())


if __name__ == "__main__":
    main()
