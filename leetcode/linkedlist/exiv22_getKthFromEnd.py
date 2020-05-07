#! /usr/local/bin/python3
from listNode import ListNode


def getKthFromEnd(head: ListNode, k: int) -> ListNode:
    node = head
    length = 0
    while node is not None:
        length += 1
        node = node.next
    node = head
    for i in range(length - k):
        node = node.next
    return node


def main():
    print(getKthFromEnd(ListNode.make([i for i in range(6)]), 3))       # 3->4->5


if __name__ == "__main__":
    main()
