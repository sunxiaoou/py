#! /usr/local/bin/python3
from listNode import ListNode


def removeDuplicateNodes(head: ListNode) -> ListNode:
    if head is None:
        return None
    ns = {head.val}
    prev = head
    curr = prev.next
    while curr is not None:
        if curr.val not in ns:
            ns.add(curr.val)
            prev = curr
        else:
            prev.next = curr.next
        curr = curr.next
    return head


def main():
    print(removeDuplicateNodes(ListNode.make([])))                  # None
    print(removeDuplicateNodes(ListNode.make([1, 2, 3, 3, 2, 1])))  # [1, 2, 3]
    print(removeDuplicateNodes(ListNode.make([1, 1, 1, 1, 2])))     # [1, 2]


if __name__ == "__main__":
    main()
