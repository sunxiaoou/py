#! /usr/local/bin/python3
from listNode import ListNode


def oddEvenList(head: ListNode) -> ListNode:
    if head is None:
        return None
    prev = head
    node = head.next
    h2 = ListNode(-1)
    even = h2
    i = 0
    while node is not None:
        if not i % 2:
            prev.next = node.next
            even.next = node
            even = node
        else:
            prev = node
        node = node.next
        i += 1
    even.next = None
    prev.next = h2.next
    return head


def main():
    print(oddEvenList(ListNode.make([])))          # 1->3->5->2->4
    print(oddEvenList(ListNode.make([1, 2, 3, 4, 5])))          # 1->3->5->2->4
    print(oddEvenList(ListNode.make([2, 1, 3, 5, 6, 4, 7])))    # 2->3->6->7->1->5->4


if __name__ == "__main__":
    main()
