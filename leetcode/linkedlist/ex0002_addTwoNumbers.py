#! /usr/local/bin/python3
from listNode import ListNode


def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    head = ListNode(-1)
    node = head
    carry = 0
    while l1 is not None and l2 is not None:
        qu, re = divmod(l1.val + l2.val + carry, 10)
        node.next = ListNode(re)
        node = node.next
        l1 = l1.next
        l2 = l2.next
        carry = qu

    if l1 is not None:
        node.next = l1
    elif l2 is not None:
        node.next = l2
    while node.next is not None:
        node = node.next
        qu, re = divmod(node.val + carry, 10)
        node.val = re
        carry = qu
    if carry:
        node.next = ListNode(1)
    return head.next


def main():
    print(addTwoNumbers(ListNode.make([3, 4, 5]), ListNode.make([4, 6, 5])))
    # 7->0->1->1
    print(addTwoNumbers(ListNode.make([1]), ListNode.make([9, 9])))     # 0->0->1


if __name__ == "__main__":
    main()
