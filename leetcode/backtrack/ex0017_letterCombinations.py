#! /usr/local/bin/python3
from typing import List


def letterCombinations(digits: str) -> List[str]:
    if not digits:
        return []
    buttons = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno',
               '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
    res = []

    def backtrack(ans: List, s: str):
        if not s:
            res.append(''.join(ans))
            return
        for ch in buttons[s[0]]:
            ans.append(ch)
            backtrack(ans, s[1:])
            ans.pop()

    backtrack([], digits)
    return res


def main():
    print(letterCombinations(""))       # []
    print(letterCombinations("23"))
    # ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]


if __name__ == "__main__":
    main()
