#! /usr/local/bin/python3
from typing import List


def generateParenthesis2_error(n: int) -> List[str]:
    if n < 1:
        return []
    if n == 1:
        return ['()']

    left = ['()' + p for p in generateParenthesis(n - 1)]
    medium = ['(' + p + ')' for p in generateParenthesis(n - 1)]
    right = [p + '()' for p in generateParenthesis(n - 1)]
    return list(set(left + medium + right))


#        root        this is a tree, for example n == 2,
#        /           traversal: root, left, l, r, r, get first answer - (())
#       left         backtrack to 'left': r, r, l, left
#      /    \        traversal: left, r, l, r, get second answer - ()()
#     l      r       backtrack to 'root': r, l, r, left, root
#      \    /
#        r l
#         \ \
#          r r


def generateParenthesis(n: int) -> List[str]:
    res = []

    def backtrack(ans: List, left: int, right: int):
        if len(ans) == n * 2:
            res.append(''.join(ans))
            return
        if left < n:
            ans.append('(')
            backtrack(ans, left + 1, right)
            ans.pop()
        if right < left:
            ans.append(')')
            backtrack(ans, left, right + 1)
            ans.pop()

    backtrack([], 0, 0)
    return res


def main():
    res = generateParenthesis(4)
    print(len(res))
    print(res)

    ans = ["(((())))", "((()()))", "((())())", "((()))()",
           "(()(()))", "(()()())", "(()())()", "(())(())",
           "(())()()", "()((()))", "()(()())", "()(())()",
           "()()(())", "()()()()"]

    print(set(res) ^ set(ans))


if __name__ == "__main__":
    main()
