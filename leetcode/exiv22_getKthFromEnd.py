#! /usr/local/bin/python3


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __str__(self):
        node = self
        s = str(node.val)
        while node.next is not None:
            node = node.next
            s += "->{}".format(str(node.val))
        return s


def getKthFromEnd(head: ListNode, k: int) -> ListNode:
    node = head
    length = 0
    while node is not None:
        length += 1
        node = node.next

    node = head
    for i in range(length - k):
        node = node.next

    return node


def main():
    head = ListNode(None)
    current_node = head
    for i in range(1, 6):
        node = ListNode(i)
        current_node.next = node
        current_node = node
    print(getKthFromEnd(head.next, 3))


if __name__ == "__main__":
    main()
