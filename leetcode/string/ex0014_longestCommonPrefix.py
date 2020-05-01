#! /usr/local/bin/python3
from typing import List


def longestCommonPrefix(strs: List[str]) -> str:
    n, j = len(strs), 0
    if n == 0:
        return ""

    while True:
        try:                    # in case one of strings is empty
            i, ch = 0, strs[0][j]
            for i in range(1, n):
                if ch != strs[i][j]:
                    break
            else:
                i = n           # continue to next j
            if i < n:
                break
            j += 1
        except IndexError:
            break
    return strs[0][: j]


def main():
    print(longestCommonPrefix([]))                              # ""
    print(longestCommonPrefix(["dog", "d", "do"]))              # "d"
    print(longestCommonPrefix(["flower", "flow", "flight"]))    # "fl"
    print(longestCommonPrefix(["dog", "racecar", "car"]))       # ""


if __name__ == "__main__":
    main()
