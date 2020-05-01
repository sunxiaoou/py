#! /usr/local/bin/python3
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

    @classmethod
    def make(cls, nums: List):
        n = len(nums)
        if n == 0:
            return None
        head = cls(nums[0])
        curr = head
        for i in range(1, n):
            curr.next = cls(nums[i])
            curr = curr.next
        return head


def main():
    print(ListNode.make([1, 2, 3, 4, 5]))     # 1->2->3->4->5


if __name__ == "__main__":
    main()
