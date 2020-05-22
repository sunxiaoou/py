#! /usr/local/bin/python3
from typing import List

from treeNode import TreeNode


def inorderTraversal(root: TreeNode) -> List[int]:
    if root is None:
        return []
    res = []
    if root.left is not None:
        res = inorderTraversal(root.left)
    res.append(root.val)
    if root.right is not None:
        res += inorderTraversal(root.right)
    return res


def main():
    print(inorderTraversal(TreeNode.make([1, None, 2, 3])))     # [1, 3, 2]
    nums = [5, 4, 1, None, 1, None, 4, 2, None, 2, None]
    print(inorderTraversal(TreeNode.make(nums)))     # [4, 2, 1, 5, 1, 2, 4]


if __name__ == "__main__":
    main()
