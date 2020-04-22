#! /usr/local/bin/python3
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def create_tree(nums: List) -> TreeNode:
    i = 0
    nodes = []
    while True:
        j = 2 ** i                      # number in current level is 2 times number in last level
        if j > len(nums):
            break
        for _ in range(j):
            k = len(nodes)              # k is index in nums
            node = TreeNode(nums[k])
            if k > 0:                   # to find out the parent
                if k % 2:
                    nodes[k // 2].left = node
                else:
                    nodes[(k - 1) // 2].right = node
            nodes.append(node)
        i += 1
    return nodes[0]


def show_tree(root: TreeNode):
    def show(node: TreeNode, lev: int):
        if node is None:
            print('\t' * lev, None)
        else:
            print('\t' * lev, node.val)
            if node.left is not None:
                show(node.left, lev + 1)
            if node.right is not None:
                show(node.right, lev + 1)
    show(root, 0)


def rightSideView(root: TreeNode) -> List[int]:
    view = {}

    def show(node: TreeNode, lev: int):
        if node is not None:
            view[lev] = node.val
            if node.left is not None:
                show(node.left, lev + 1)
            if node.right is not None:
                show(node.right, lev + 1)

    show(root, 0)
    # print(view)
    return list(view.values())


def main():
    nums = [1, 2, 3, None, 5, None, 4]
    root = create_tree(nums)
    # show_tree(root)
    print(rightSideView(root))      # [1, 3, 4]


if __name__ == "__main__":
    main()
