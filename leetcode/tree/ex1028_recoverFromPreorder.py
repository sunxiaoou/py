#! /usr/local/bin/python3
from treeNode import TreeNode


def recoverFromPreorder(S: str) -> TreeNode:
    # print(S)
    n = len(S)
    i = 0
    while S[i] == "-":
        i += 1
    j = i
    while j < n and S[j] != "-":
        j += 1
    root = TreeNode(int(S[i: j]))
    if j == n:
        return root

    i = j
    while S[i] == "-":
        i += 1
    d, j = i - j, i             # d is depth of left child, i is start index of left child

    count = 0
    while j < n:
        if S[j] != "-":
            if count == d:
                break
            count = 0
        else:
            count += 1
        j += 1                  # j is start index of right child

    root.left = recoverFromPreorder(S[i: j].rstrip('-'))
    if j < n:                   # if right child exists
        root.right = recoverFromPreorder(S[j:])
    return root


def main():
    print(recoverFromPreorder("1-2--3---4-5--6---7").print())
    print(recoverFromPreorder("12").print())
    print(recoverFromPreorder("1-2--3--4-5--6--7").print())
    print(recoverFromPreorder("1-401--349---90--88").print())


if __name__ == "__main__":
    main()
