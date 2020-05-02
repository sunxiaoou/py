#! /usr/local/bin/python3
from typing import List


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __str__(self):
        res, curr = '', self
        while curr is not None:
            res += str(curr.val)
            curr = curr.next
            if curr is not None:
                res += '->'
        return res

    @classmethod
    def make(cls, nums: List):
        n, dummy = len(nums), cls(-42)
        curr = dummy
        for i in range(n):
            curr.next = cls(nums[i])
            curr = curr.next
        return dummy.next


def main():
    print(ListNode.make([1, 2, 3, 4, 5]))     # 1->2->3->4->5


if __name__ == "__main__":
    main()
