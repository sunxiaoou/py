#! /usr/local/bin/python3
from treeNode import TreeNode


def hasPathSum(root: TreeNode, sum: int) -> bool:
    if root is None:
        return False
    if root.left is None and root.right is None:
        return root.val == sum
    if root.left is not None and hasPathSum(root.left, sum - root.val):
        return True
    if root.right is not None and hasPathSum(root.right, sum - root.val):
        return True
    return False


def main():
    print(hasPathSum(TreeNode.make([]), 0))     # False
    print(hasPathSum(TreeNode.make([3, 4, 5, 1, 2, None, None, None, None, 0]), 9))     # True
    print(hasPathSum(TreeNode.make([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]), 22))
    # True


if __name__ == "__main__":
    main()
