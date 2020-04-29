#! /usr/local/bin/python3
from bisect import insort
from typing import List


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __str__(self):
        res, head = '', self
        while head is not None:
            res += str(head.val)
            head = head.next
            if head is not None:
                res += '->'
        return res


def crt_linked(nums: List) -> ListNode:
    n = len(nums)
    head = ListNode(nums[0])
    curr = head
    for i in range(1, n):
        curr.next = ListNode(nums[i])
        curr = curr.next
    return head


def mergeKLists(lists: List[ListNode]) -> ListNode:
    nums = []
    for head in lists:
        while head is not None:
            insort(nums, head.val)
            head = head.next
    return crt_linked(nums)


def main():
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    print(mergeKLists([crt_linked(i) for i in lists]))


if __name__ == "__main__":
    main()
