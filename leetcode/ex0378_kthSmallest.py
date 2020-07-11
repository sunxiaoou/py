#! /usr/local/bin/python3
from typing import List


def kthSmallest(matrix: List[List[int]], k: int) -> int:
    m2 = []
    for i in matrix:
        m2 += i
    return sorted(m2)[k - 1]


def main():
    matrix = [[1,  5,  9],
              [10, 11, 13],
              [12, 13, 15]]
    print(kthSmallest(matrix, 8))


if __name__ == "__main__":
    main()
