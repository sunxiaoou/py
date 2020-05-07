#! /usr/local/bin/python3
from typing import List
from listNode import ListNode


def list2linked(nums: List[int]) -> ListNode:
    head = ListNode(nums[0])
    curr = head
    for i in range(1, len(nums)):
        curr.next = ListNode(nums[i])
        curr = curr.next
    return head


def linked2list(head: ListNode) -> List[int]:
    nums = []
    while head is not None:
        nums.append(head.val)
        head = head.next
    return nums


def linked2num(head: ListNode) -> int:
    num = 0
    while head is not None:
        num = num * 10 + head.val
        head = head.next
    return num


def num2linked(num: int) -> ListNode:
    if not num:
        return ListNode(0)
    curr = None
    while num:
        node = ListNode(num % 10)
        if curr is not None:
            node.next = curr
        curr = node
        num //= 10
    return curr


def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    num = linked2num(l1) + linked2num(l2)
    return num2linked(num)


def test(n1: List[int], n2: List[int]):
    l1 = list2linked(n1)
    l2 = list2linked(n2)
    print(linked2list(addTwoNumbers(l1, l2)))


def main():
    test([7, 2, 4, 3], [5, 6, 4])       # [7, 8, 0, 7]
    test([5, 6, 4], [0])                # [5, 6, 4]
    test([0], [0])                      # [0]


if __name__ == "__main__":
    main()
