#! /usr/local/bin/python3
from treeNode import TreeNode


def isValidBST(root: TreeNode) -> bool:
    prev = None

    def traversal(root: TreeNode) -> bool:
        nonlocal prev
        if root is None:
            return True
        flag = traversal(root.left)
        # print(prev, root.val)
        if prev is not None and root.val <= prev:
            return False
        prev = root.val
        return flag and traversal(root.right)

    return traversal(root)


def main():
    print(isValidBST(TreeNode.make([-2147483648])))                     # True
    print(isValidBST(TreeNode.make([1, 1])))                            # False
    print(isValidBST(TreeNode.make([2, 1, 3])))                         # True
    print(isValidBST(TreeNode.make([5, 1, 4, None, None, 3, 6])))       # False
    print(isValidBST(TreeNode.make([10, 5, 15, None, None, 6, 20])))    # False


if __name__ == "__main__":
    main()
