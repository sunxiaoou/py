#! /usr/local/bin/python3
from typing import List


def hasGroupsSizeX(deck: List[int]) -> bool:
    d2 = sorted(deck)
    for x in range(2, len(d2) + 1):
        if len(d2) % x == 0:
            for i in range(len(d2) // x):
                sub = d2[i * x: (i + 1) * x]
                # print(sub, end=' ')
                if sub.count(sub[0]) != x:
                    break
            else:
                # print()
                return True
            # print()
    return False


def main():
    print(hasGroupsSizeX([1, 2, 3, 4, 4, 3, 2, 1]))
    print(hasGroupsSizeX([1, 1, 1, 2, 2, 2, 3, 3]))
    print(hasGroupsSizeX([1]))
    print(hasGroupsSizeX([1, 1]))
    print(hasGroupsSizeX([1, 1, 2, 2, 2, 2]))


if __name__ == "__main__":
    main()
