#! /usr/local/bin/python3
from listNode import ListNode


def isPalindrome(head: ListNode) -> bool:
    n, curr = 0, head
    while curr is not None:                 # get linked list length
        n += 1
        curr = curr.next

    mid = n // 2                            # reverse first half part
    prev, curr = None, head
    for i in range(mid):
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next

    if n % 2 == 1:                          # if length is odd, skip middle node
        curr = curr.next

    for i in range(mid):                    # compare first and second part
        if prev.val != curr.val:
            return False
        prev = prev.next
        curr = curr.next
    return True


def main():
    print(isPalindrome(ListNode.make([1])))                 # False
    print(isPalindrome(ListNode.make([1, 2])))              # False
    print(isPalindrome(ListNode.make([1, 2, 2, 1])))        # True
    print(isPalindrome(ListNode.make([1, 2, 3, 2, 1])))     # True


if __name__ == "__main__":
    main()
