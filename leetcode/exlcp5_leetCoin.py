#! /usr/local/bin/python3
# https://leetcode-cn.com/problems/coin-bonus/
from typing import List


class TreeNode:
    def __init__(self, x):
        self.id = x
        self.val = 0
        self.next_sibling = None
        self.first_child = None
        self.last_child = None


def print_tree(parent: TreeNode, depth: int):
    print('\t' * depth, parent.id, parent.val)
    if parent.first_child is not None:
        child = parent.first_child
        while child is not None:
            print_tree(child, depth + 1)
            child = child.next_sibling


def grant_tree(parent: TreeNode, amount: int):
    parent.val += amount
    child = parent.first_child
    while child is not None:
        grant_tree(child, amount)
        child = child.next_sibling


def count_tree(parent: TreeNode) -> int:
    summary = parent.val
    child = parent.first_child
    while child is not None:
        summary += count_tree(child)
        child = child.next_sibling
    return summary


def bonus(leadership: List[List[int]], operations: List[List[int]]) -> List[int]:
    nodes = {}
    for le in leadership:
        if le[0] not in nodes:
            parent = TreeNode(le[0])
            nodes[le[0]] = parent
        else:
            parent = nodes[le[0]]
        if le[1] not in nodes:
            child = TreeNode(le[1])
            nodes[le[1]] = child
        else:
            child = nodes[le[1]]
        if parent.first_child is None:
            parent.first_child = parent.last_child = child
        else:
            parent.last_child.next_sibling = child
            parent.last_child = child

    result = []
    for op in operations:
        parent = nodes[op[1]]
        if op[0] == 1:
            parent.val += op[2]
        elif op[0] == 2:
            grant_tree(parent, op[2])
        elif op[0] == 3:
            result.append(count_tree(parent) % 1000000007)

    print_tree(nodes[1], 0)
    return result


def main():
    leadership = [[1, 2], [1, 6], [2, 3], [2, 5], [1, 4]]
    operations = [[1, 1, 500], [2, 2, 50], [3, 1], [2, 6, 15], [3, 1]]
    print(bonus(leadership, operations))    # [650, 665]


if __name__ == "__main__":
    main()
