#! /usr/local/bin/python3
from collections import deque
from typing import List
from treeNode import TreeNode


def levelOrder(root: TreeNode) -> List[List[int]]:
    if root is None:
        return []
    # print(root.show())
    res, vals = [], []
    curr_level = 0
    bfs = deque()
    bfs.append((root, curr_level))
    while bfs:
        node, level = bfs.popleft()
        if level != curr_level:
            res.append(vals)
            vals = []
            curr_level = level
        vals.append(node.val)
        if node.left is not None:
            bfs.append((node.left, level + 1))
        if node.right is not None:
            bfs.append((node.right, level + 1))
    if vals:
        res.append(vals)
    return res


def main():
    print(levelOrder(TreeNode.make([3, 9, 20, None, None, 15, 7])))     # [[3], [9, 20], [15, 7]]
    print(levelOrder(TreeNode.make([])))                                # []


if __name__ == "__main__":
    main()
