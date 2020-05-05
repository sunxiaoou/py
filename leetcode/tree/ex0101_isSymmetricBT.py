#! /usr/local/bin/python3
from treeNode import TreeNode


def isSymmetric(root: TreeNode) -> bool:

    def mirror(t1: TreeNode, t2: TreeNode) -> bool:
        if t1 is None and t2 is None:       # both t1, t2 are None
            return True
        if t1 is None or t2 is None:        # either t1 or t2 is None
            return False
        # neither t1 nor t2 is None
        return t1.val == t2.val and mirror(t1.left, t2.right) and mirror(t1.right, t2.left)

    return mirror(root, root)


def main():
    print(isSymmetric(TreeNode.make([5, 4, 1, None, 1, None, 4, 2, None, 2, None])))    # False
    print(isSymmetric(TreeNode.make([1, 2, 2, 3, 4, 4, 3])))                            # True
    print(isSymmetric(TreeNode.make([1, 2, 2, None, 3, None, 3])))                      # False


if __name__ == "__main__":
    main()
