#! /usr/local/bin/python3
from collections import deque

from treeNode import TreeNode


class Codec:
    def serialize(self, root: TreeNode) -> str:
        if root is None:
            return "[]"
        s = [str(root.val)]
        bfs = deque()
        bfs.append(root)
        while bfs:
            node = bfs.popleft()
            if node.left is None:
                s.append("null")
            else:
                s.append(str(node.left.val))
                bfs.append(node.left)
            if node.right is None:
                s.append("null")
            else:
                s.append(str(node.right.val))
                bfs.append(node.right)
        for i in range(len(s) - 1, -1, -1):
            if s[i] != "null":
                break
        return "[" + ",".join(s[: i + 1]) + "]"

    def deserialize(self, data: str) -> TreeNode:
        if data == "[]":
            return None
        s = data.strip("[]").split(",")
        root = TreeNode(int(s[0]))
        bfs = deque()
        bfs.append(root)
        n, i = len(s), 1
        while bfs:
            node = bfs.popleft()
            if i < n:
                if s[i] != "null":
                    node.left = TreeNode(int(s[i]))
                    bfs.append(node.left)
                i += 1
            else:
                break
            if i < n:
                if s[i] != "null":
                    node.right = TreeNode(int(s[i]))
                    bfs.append(node.right)
                i += 1
            else:
                break
        return root


def main():
    codec = Codec()
    root = codec.deserialize("[]")
    root = codec.deserialize("[1,2,3,null,null,4,5]")
    print(root.print())
    print(codec.serialize(root))


if __name__ == "__main__":
    main()
