#! /usr/local/bin/python3
from typing import List
from listNode import ListNode


def deleteNode(node: ListNode):         # the node cannot be last one, so we can
    node.val = node.next.val            # set next node value to this one
    node.next = node.next.next          # then remove next node, this is tricky


def test(nums: List[int], val: int) -> None:
    head = ListNode.make(nums)
    node = head
    while node is not None:
        if node.val == val:
            break
        node = node.next
    else:
        return
    deleteNode(node)
    print(head)


def main():
    test([4, 5, 1, 9], 5)       # 4->1->9
    test([4, 5, 1, 9], 1)       # 4->5->9


if __name__ == "__main__":
    main()
