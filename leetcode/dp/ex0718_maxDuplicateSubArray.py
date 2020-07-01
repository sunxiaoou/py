#! /usr/local/bin/python3
from typing import List


def findLength(A: List[int], B: List[int]) -> int:
    m, n = len(A), len(B)
    dp = [[0] * m for _ in range(n)]

    for i in range(m):
        for j in range(n):
            if A[j] == B[i]:
                dp[i][j] = dp[i - 1][j - 1] + 1 if i and j else 1

    # for i in dp:
    #    print(i)
    return max(max(i) for i in dp)


def main():
    print(findLength([0, 0, 0, 0, 1], [1, 0, 0, 0, 0]))     # 4
    print(findLength([1, 2, 3, 2, 1], [3, 2, 1, 4, 7]))     # 3


if __name__ == "__main__":
    main()
