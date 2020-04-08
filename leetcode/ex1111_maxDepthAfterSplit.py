#! /usr/local/bin/python3
# https://leetcode-cn.com/problems/maximum-nesting-depth-of-two-valid-parentheses-strings/
from typing import List


def maxDepthAfterSplit(seq: str) -> List[int]:
    stack = []
    result = []
    for ch in seq:
        if ch == '(':
            stack.append(ch)
            result.append(0 if len(stack) % 2 != 0 else 1)
            # result.append(len(stack))
        elif ch == ')':
            # result.append(len(stack))
            result.append(0 if len(stack) % 2 != 0 else 1)
            stack.pop()
    return result


def main():
    print(maxDepthAfterSplit("(()())"))
    print(maxDepthAfterSplit("()(())()"))
    pass


if __name__ == "__main__":
    main()
