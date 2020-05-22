#! /usr/local/bin/python3
from typing import List

from treeNode import TreeNode


def zigzagLevelOrder(root: TreeNode) -> List[List[int]]:
    # print(root.show())
    res = []

    def level_order(root: TreeNode, depth: int):
        if root is None:
            return
        if len(res) <= depth:
            res.append([root.val])
        else:
            res[depth].append(root.val)
        level_order(root.left, depth + 1)
        level_order(root.right, depth + 1)

    level_order(root, 0)
    for i in range(len(res)):
        if i % 2:
            res[i] = res[i][:: -1]
    return res


def main():
    print(zigzagLevelOrder(TreeNode.make([3, 9, 20, None, None, 15, 7])))
    # [[3], [20, 9], [15, 7]]


if __name__ == "__main__":
    main()
