#! /usr/local/bin/python3
from typing import List
from listNode import ListNode


# double pA and pB, traversal A + B and B + A respectively,
# as A + B = B + A, they will encounter at the intersection node
# or None if there is no intersection at all
def getIntersectionNode(headA: ListNode, headB: ListNode) -> ListNode:
    pa, pb = headA, headB
    while pa != pb:
        pa = headB if pa is None else pa.next
        pb = headA if pb is None else pb.next
    return pa


def test(n1: List[int], n2: List[int], s1: int, s2: int) -> None:
    h1 = ListNode.make(n1[: s1])
    t1 = h1
    while t1.next is not None:
        t1 = t1.next
    h2 = ListNode.make(n2[: s2])
    t2 = h2
    while t2.next is not None:
        t2 = t2.next
    h3 = ListNode.make(n1[s1:])
    t1.next = t2.next = h3
    # print(h1, h2)
    print(getIntersectionNode(h1, h2))


def main():
    test([4, 1, 8, 4, 5], [5, 0, 1, 8, 4, 5], 2, 3)
    test([2, 6, 4], [1, 5], 3, 2)


if __name__ == "__main__":
    main()
