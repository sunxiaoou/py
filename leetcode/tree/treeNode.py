#! /usr/local/bin/python3
from collections import deque
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.val) if self is not None else 'None'

    def find(self, val: int):

        def traversal(root: TreeNode, val: int):
            if root.val == val:
                return root
            node = None
            if root.left is not None:
                node = traversal(root.left, val)
            if node is None and root.right is not None:
                node = traversal(root.right, val)
            return node

        return traversal(self, val)

    def pre_order(self):
        res = []

        def traversal(root: TreeNode):
            if root is None:
                res.append(None)
                return
            res.append(root.val)
            if root.left is not None:
                traversal(root.left)
            if root.right is not None:
                traversal(root.right)

        traversal(self)
        # return [i for i in res if i is not None]
        return res

    def in_order(self):
        res = []

        def traversal(root: TreeNode):
            if root is None:
                res.append(None)
                return
            if root.left is not None:
                traversal(root.left)
            res.append(root.val)
            if root.right is not None:
                traversal(root.right)

        traversal(self)
        return res

    def post_order(self):
        res = []

        def traversal(root: TreeNode):
            if root is None:
                res.append(None)
                return
            if root.left is not None:
                traversal(root.left)
            if root.right is not None:
                traversal(root.right)
            res.append(root.val)

        traversal(self)
        return res

    def show(self):
        string = ''

        def traversal(node: TreeNode, lev: int):
            nonlocal string

            if node is None:
                string += '\t' * lev + 'None\n'
            else:
                string += '\t' * lev + str(node.val) + '\n'
                if node.left is not None or node.right is not None:
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
        if not nums:
            return None
        nodes = deque()
        root = cls(nums[0])
        nodes.append(root)
        i, n = 0, len(nums)
        while nodes:
            node = nodes.popleft()
            if node is not None:
                i += 1
                if i < n:
                    node.left = None if nums[i] is None else cls(nums[i])
                    nodes.append(node.left)
                else:
                    break
                i += 1
                if i < n:
                    node.right = None if nums[i] is None else cls(nums[i])
                    nodes.append(node.right)
                else:
                    break
        return root


def main():
    # root = TreeNode.make([1, 2, 3, None, 5, None, 4])
    # root = TreeNode.make2([10, 5, 15, None, None, 6, 20])
    # print(root.show())
    # root = TreeNode.make([10, 5, 15, None, None, 6, 20])
    # root = TreeNode.make([0, None, 2, 5, 6])
    root = TreeNode.make([5, 4, 1, None, 1, None, 4, 2, None, 2, None])
    root = TreeNode.make([3, 9, 20, None, None, 15, 7])
    print(root.show())
    print(root.pre_order())
    print(root.in_order())
    print(root.post_order())
    print(root.find(20).show())
    # print(root.find())
    # print(root.minimum())


if __name__ == "__main__":
    main()
