#! /usr/local/bin/python3
from treeNode import TreeNode


def isSubtree(s: TreeNode, t: TreeNode) -> bool:

    def is_same(a: TreeNode, b: TreeNode) -> bool:
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        return a.val == b.val and is_same(a.left, b.left) and is_same(a.right, b.right)

    if is_same(s, t):
        return True
    le = s.left is not None and isSubtree(s.left, t)
    ri = s.right is not None and isSubtree(s.right, t)
    return le or ri


def main():
    print(isSubtree(TreeNode.make([1, 1]), TreeNode.make([1])))      # True
    print(isSubtree(TreeNode.make([3, 4, 5, 1, 2]), TreeNode.make([4, 1, 2])))      # True
    print(isSubtree(TreeNode.make([3, 4, 5, 1, 2, None, None, None, None, 0]),
                    TreeNode.make([4, 1, 2])))      # False


if __name__ == "__main__":
    main()
