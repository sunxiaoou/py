#! /usr/local/bin/python3
from typing import List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    @staticmethod
    def preorder_traversal(node):
        print(node.val, end=', ')
        if node.left is not None:
            node.preorder_traversal(node.left)
        if node.right is not None:
            node.preorder_traversal(node.right)


def buildTree(preorder: List[int], inorder: List[int]) -> TreeNode:
    if not preorder:
        return None

    node = TreeNode(preorder[0])
    if len(preorder) == 1:
        return node

    i = inorder.index(node.val)
    node.left = buildTree(preorder[1: i + 1], inorder[: i])
    node.right = buildTree(preorder[i + 1:], preorder[i + 1:])

    return node


def main():
    node = buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    TreeNode.preorder_traversal(node)

if __name__ == "__main__":
    main()
