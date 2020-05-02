#! /usr/local/bin/python3
from typing import List
from listNode import ListNode


def hasCycle(head: ListNode) -> bool:
    dictionary = {}
    curr = head
    while curr is not None:
        if curr in dictionary:
            return True
        dictionary[curr] = curr.val
        curr = curr.next
    return False


def get_linked(nums: List[int], pos: int) -> ListNode:
    n, dummy = len(nums), ListNode(-1)
    curr = dummy
    temp = tail = None
    for i in range(n):
        curr.next = ListNode(nums[i])
        curr = curr.next
        if pos == i:
            temp = curr
        if i == n - 1:
            tail = curr
    if pos >= 0:
        tail.next = temp
    return dummy.next


def main():
    print(hasCycle(get_linked([3, 2, 0, -4], 1)))           # True
    print(hasCycle(get_linked([1, 2], 0)))                  # True
    print(hasCycle(get_linked([1], -1)))                    # False


if __name__ == "__main__":
    main()
