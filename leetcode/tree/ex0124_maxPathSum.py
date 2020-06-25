#! /usr/local/bin/python3
from treeNode import TreeNode


def maxPathSum(root: TreeNode) -> int:
    # print(root.show())
    maxi = -float('inf')

    def traversal(root: TreeNode) -> int:
        nonlocal maxi
        if root is None:
            return 0
        le = max(0, traversal(root.left))           # if le < 0, ignore it as 0
        ri = max(0, traversal(root.right))          # if ri < 0, ignore it as 0
        lmr = le + root.val + ri                    # path le - root - ri
        ret = max(root.val + le, root.val + ri)     # ret is bigger sum between le - root and ri - root
        maxi = max(maxi, lmr, ret)                  # update maxi from lmr, le - root and ri - root
        return ret

    traversal(root)
    return maxi


def main():
    print(maxPathSum(TreeNode.make([-2, -1, -1])))                      # 10
    print(maxPathSum(TreeNode.make([1, 2, 3, 4])))                      # 10
    print(maxPathSum(TreeNode.make([1, -2, -3, 1, 3, -1, None, -1])))   # 3
    print(maxPathSum(TreeNode.make([1, 2, 3])))                         # 6
    print(maxPathSum(TreeNode.make([-10, 9, 20, None, None, 15, 7])))   # 42


if __name__ == "__main__":
    main()
