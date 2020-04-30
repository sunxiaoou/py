#! /usr/local/bin/python3
from typing import List


def reverseString(s: List[str]) -> None:
    n = len(s)
    left, right = 0, n - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1


def main():
    s = ["h", "e", "l", "l", "o"]
    # s = ["H", "a", "n", "n", "a", "h"]
    reverseString(s)
    print(s)


if __name__ == "__main__":
    main()
