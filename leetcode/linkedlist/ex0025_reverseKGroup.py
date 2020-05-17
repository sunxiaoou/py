#! /usr/local/bin/python3
from listNode import ListNode


def reverseKGroup(head: ListNode, k: int) -> ListNode:
    node = head
    n = 0
    while node is not None:         # get length of linked list
        node = node.next
        n += 1
    last_tail = curr_head = head    # last group tail and current group head point to head
    for i in range(n // k):         # n // k is number of groups
        prev, node = None, curr_head
        for j in range(k):          # reverse current group one by one
            tmp = node.next         # keep next node
            node.next = prev        # current node links to prev node as next node
            prev = node             # prev moves forward, becomes new head finally
            node = tmp              # current node moves forward
        # print(last_tail.val, curr_head.val, prev.val, node.val)
        if not i:
            head = prev             # head points to new head of first group
        last_tail.next = prev       # last group tail points to current group new head
        last_tail = curr_head       # update last_tail to current group tail (original head)
        curr_head.next = node       # current group tail links to next node
        curr_head = node            # reset current group head as next group head
    return head


def main():
    print(reverseKGroup(ListNode.make([1, 2, 3, 4, 5]), 2))     # 2->1->4->3->5
    print(reverseKGroup(ListNode.make([1, 2, 3, 4, 5]), 3))     # 3->2->1->4->5


if __name__ == "__main__":
    main()
