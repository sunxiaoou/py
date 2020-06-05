#! /usr/local/bin/python3
from treeNode import TreeNode


def kthSmallest(root: TreeNode, k: int) -> int:
    inorder = []

    def travrsal(root: TreeNode):
        if root.left is not None:
            travrsal(root.left)
        inorder.append(root.val)
        if root.right is not None:
            travrsal(root.right)

    travrsal(root)
    # print(inorder)
    return inorder[k - 1]


def main():
    print(kthSmallest(TreeNode.make([3, 1, 4, None, 2]), 1))                # 1
    print(kthSmallest(TreeNode.make([5, 3, 6, 2, 4, None, None, 1]), 3))    # 3


if __name__ == "__main__":
    main()
