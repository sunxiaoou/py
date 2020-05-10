#! /usr/local/bin/python3
from typing import List
from treeNode import TreeNode


def commonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:

    def traversal(tree: TreeNode, node: TreeNode, ans: List[TreeNode]):
        if tree == node:                # found given node
            ans.append(tree)
            return
        if not ans and tree.left is not None:
            traversal(tree.left, node, ans)
        if not ans and tree.right is not None:
            traversal(tree.right, node, ans)
        if ans:                         # append ancestor one by one
            ans.append(tree)

    a1 = []
    traversal(root, p, a1)
    a2 = []
    traversal(root, q, a2)
    if not a1 or not a2:
        return None
    i, j = len(a1) - 1, len(a2) - 1
    while i >= 0 and j >= 0 and a1[i] == a2[j]:
        i -= 1
        j -= 1
    return a1[i + 1]


def main():

    def test(nums: List[int], p: int, q: int) -> TreeNode:
        root = TreeNode.make(nums)
        # print(root.show())
        node = commonAncestor(root, root.find(p), root.find(q))
        return node.val

    print(test([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 1))      # 3
    print(test([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 4))      # 5


if __name__ == "__main__":
    main()
