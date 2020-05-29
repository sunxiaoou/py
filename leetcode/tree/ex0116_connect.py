#! /usr/local/bin/python3
import json
from pprint import pprint


class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None,
                 next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

    def print(self):
        string = ''

        def traversal(node: Node, lev: int):
            nonlocal string

            if node is None:
                string += '\t' * lev + 'None\n'
            else:
                string += '\t' * lev + str(node.val) + '\n'
                if node.left is not None or node.right is not None:
                    traversal(node.left, lev + 1)
                if node.right is not None:
                    traversal(node.right, lev + 1)

        traversal(self, 0)
        return string

    @classmethod
    def dump(cls, root: 'Node') -> dict:
        return {'val': root.val,
                'left': None if root.left is None else cls.dump(root.left),
                'right': None if root.right is None else cls.dump(root.right),
                'next': None if root.next is None else root.next.val}

    @classmethod
    def make(cls, dic: dict):
        if not dic:
            return None
        root = cls(dic["val"])
        if dic["left"] is not None:
            root.left = cls.make(dic["left"])
        if dic["right"] is not None:
            root.right = cls.make(dic["right"])
        return root


def connect(root: Node) -> Node:
    res = []

    def traversal(root: Node, depth: int):
        if len(res) < depth + 1:
            ans = [root]
            res.append(ans)
        else:
            res[depth][-1].next = root
            res[depth].append(root)
        if root.left is not None:
            traversal(root.left, depth + 1)
        if root.right is not None:
            traversal(root.right, depth + 1)

    if root is not None:
        traversal(root, 0)
    return root


def main():
    input = '''
        {"$id":"1",
         "left":{
            "$id":"2",
             "left": {"$id":"3", "left":null, "next":null, "right":null, "val":4},
             "next":null,
             "right": {"$id":"4", "left":null, "next":null, "right":null, "val":5},
             "val":2},
         "next":null,
         "right":{
             "$id":"5",
             "left":{"$id":"6","left":null,"next":null,"right":null,"val":6},
             "next":null,
             "right":{"$id":"7","left":null,"next":null,"right":null,"val":7},
             "val":3},
         "val":1}
    '''
    root = Node.make(json.loads(input))
    root = connect(root)
    print(root.print())
    pprint(Node.dump(root))


if __name__ == "__main__":
    main()
