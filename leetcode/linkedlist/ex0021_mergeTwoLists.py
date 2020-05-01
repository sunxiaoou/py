#! /usr/local/bin/python3
from bisect import insort
from listNode import ListNode


def mergeTwoLists2(l1: ListNode, l2: ListNode) -> ListNode:
    nums = []
    for head in [l1, l2]:
        while head is not None:
            insort(nums, head.val)
            head = head.next
    return ListNode.make(nums)


def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    i, j = l1, l2
    if i is None:
        return j
    if j is None:
        return i

    if i.val > j.val:                   # ensure l1.val < l2.val
        return mergeTwoLists(l2, l1)

    while j is not None:
        if i.next is None:
            i.next = j
            break
        if j.val <= i.next.val:
            nextj = j.next
            j.next = i.next
            i.next = j
            j = nextj
        else:
            i = i.next
    return l1


def main():
    print(mergeTwoLists(ListNode.make([1, 2, 4]), ListNode.make([1, 3, 4])))        # 1->1->2->3->4->4
    print(mergeTwoLists(ListNode.make([]), ListNode.make([])))                      # None
    print(mergeTwoLists(ListNode.make([2]), ListNode.make([1])))                    # 1->2


if __name__ == "__main__":
    main()
