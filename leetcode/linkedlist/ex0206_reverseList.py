#! /usr/local/bin/python3
from listNode import ListNode


def reverseList(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr is not None:
        next = curr.next            # save next node
        curr.next = prev            # curr.next point to prev node
        prev = curr                 # set prev as curr and curr as next for next loop
        curr = next
    return prev


def main():
    print(reverseList(ListNode.make([1, 2, 3, 4, 5])))      # 5->4->3->2->1


if __name__ == "__main__":
    main()
