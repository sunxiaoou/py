#! /usr/local/bin/python3
from treeNode import TreeNode


def maxDepth2(root: TreeNode) -> int:
    if root is None:
        return 0
    res = 0

    def traversal(node: TreeNode, depth: int):
        nonlocal res
        res = max(res, depth)
        if node.left is not None:
            traversal(node.left, depth + 1)
        if node.right is not None:
            traversal(node.right, depth + 1)

    traversal(root, 1)
    return res


def maxDepth(root: TreeNode) -> int:
    if root is None:
        return 0
    return max(maxDepth(root.left), maxDepth(root.right)) + 1


def main():
    print(maxDepth(TreeNode.make([3, 9, 20, None, None, 15, 7])))       # 3
    print(maxDepth(TreeNode.make([])))                                  # 3


if __name__ == "__main__":
    main()
