#! /usr/local/bin/python3
from typing import List
from treeNode import TreeNode


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
    return list(view.values())


def main():
    root = TreeNode.make([1, 2, 3, None, 5, None, 4])
    print(rightSideView(root))      # [1, 3, 4]


if __name__ == "__main__":
    main()
