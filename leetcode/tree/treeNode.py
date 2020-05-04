#! /usr/local/bin/python3
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.val) if self is not None else 'None'

    def show(self):
        string = ''

        def traversal(node: TreeNode, lev: int):
            nonlocal string

            if node is None:
                string += '\t' * lev + 'None\n'
            else:
                string += '\t' * lev + str(node.val) + '\n'
                if node.left is not None:
                    traversal(node.left, lev + 1)
                if node.right is not None:
                    traversal(node.right, lev + 1)

        traversal(self, 0)
        return string

    def minimum(self) -> int:
        if self.left is None and self.right is None:
            return self.val
        ml = mr = float('inf')
        if self.left is not None:
            ml = self.left.minimum()
        if self.right is not None:
            mr = self.right.minimum()
        return min(self.val, ml, mr)

    @classmethod
    def make(cls, nums: List):
        i = 0
        nodes = []
        while True:
            j = 2 ** i                      # number in current level is 2 times number in last level
            if j > len(nums):
                break
            for _ in range(j):
                k = len(nodes)              # k is index in nums
                if k >= len(nums):
                    break
                node = cls(nums[k]) if nums[k] is not None else None
                if k > 0:                   # to find out the parent
                    if k % 2:
                        nodes[k // 2].left = node
                    else:
                        nodes[(k - 1) // 2].right = node
                nodes.append(node)
            i += 1
        return nodes[0] if nodes else None


def main():
    # root = TreeNode.make([1, 2, 3, None, 5, None, 4])
    root = TreeNode.make([10, 5, 15, None, None, 6, 20])
    print(root.show())
    print(root.minimum())


if __name__ == "__main__":
    main()
