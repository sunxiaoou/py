#! /usr/local/bin/python3
from typing import List


def divingBoard(shorter: int, longer: int, k: int) -> List[int]:
    if not k:
        return []
    s = shorter * k
    res = [s]
    if shorter == longer:
        return res
    for i in range(k):
        s += longer - shorter
        res.append(s)
    return res


def main():
    print(divingBoard(1, 1, 0))         # []
    print(divingBoard(1, 1, 2))         # [2]
    print(divingBoard(1, 2, 3))         # [3, 4, 5, 6]


if __name__ == "__main__":
    main()
