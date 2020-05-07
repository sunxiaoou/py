#! /usr/local/bin/python3
from bisect import insort
from typing import List
from listNode import ListNode


def mergeKLists(lists: List[ListNode]) -> ListNode:
    nums = []
    for head in lists:
        while head is not None:
            insort(nums, head.val)
            head = head.next
    return ListNode.make(nums)


def main():
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    print(mergeKLists([ListNode.make(i) for i in lists]))       # 1->1->2->3->4->4->5->6


if __name__ == "__main__":
    main()
