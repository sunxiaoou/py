#! /usr/local/bin/python3
from typing import List
from treeNode import TreeNode


def buildTree(preorder: List[int], inorder: List[int]) -> TreeNode:
    if not preorder:
        return None

    node = TreeNode(preorder[0])
    if len(preorder) == 1:
        return node

    i = inorder.index(node.val)
    node.left = buildTree(preorder[1: i + 1], inorder[: i])
    node.right = buildTree(preorder[i + 1:], inorder[i + 1:])

    return node


def main():
    root = buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    print(root.show())
    print(root.pre_order(), root.in_order())


if __name__ == "__main__":
    main()
