#! /usr/local/bin/python3
from listNode import ListNode


def removeNthFromEnd2(head: ListNode, n: int) -> ListNode:
    dummy = ListNode(-1)
    dummy.next = head
    node, i, dictionary = dummy, 0, {}
    while node is not None:
        dictionary[i] = node
        i = i + 1
        node = node.next
    # print(i)
    prev = dictionary[i - 1 - n]
    prev.next = prev.next.next
    return dummy.next                       # cannot return head as it can be removed


def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    dummy = ListNode(-1)
    dummy.next = head
    node, i = dummy, 0
    while node is not None:
        i = i + 1
        node = node.next
    n = i - n - 1                           # convert to nth from head
    node = dummy
    for i in range(n):
        node = node.next
    node.next = node.next.next
    return dummy.next                       # cannot return head as it can be removed


def main():
    print(removeNthFromEnd(ListNode.make([1, 2, 3, 4, 5]), 2))      # 1->2->3->5
    print(removeNthFromEnd(ListNode.make([1, 2]), 2))               # 2
    print(removeNthFromEnd(ListNode.make([1]), 1))                  # None


if __name__ == "__main__":
    main()
