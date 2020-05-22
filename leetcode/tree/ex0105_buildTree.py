#! /usr/local/bin/python3
from typing import List

from treeNode import TreeNode


def buildTree(preorder: List[int], inorder: List[int]) -> TreeNode:
    if not preorder:
        return None
    root = TreeNode(preorder[0])
    if len(preorder) == 1:
        return root

    i = inorder.index(preorder[0])
    root.left = buildTree(preorder[1: 1 + i], inorder[0 : i])
    root.right = buildTree(preorder[1 + i:], inorder[i + 1:])
    return root


def main():
    print(buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]).show())
    print(buildTree([1, 2], [1, 2]).show())


if __name__ == "__main__":
    main()
