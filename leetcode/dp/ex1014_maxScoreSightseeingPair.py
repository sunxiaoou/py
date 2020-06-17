#! /usr/local/bin/python3
from typing import List


def maxScoreSightseeingPair_slow(A: List[int]):
    n = len(A)
    res = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            res = max(res, A[i] + A[j] + i - j)
    return res


# A[i] + A[j] + i - j convert to A[i] + i + A[j] - j
#      0  1  2  3  4
# A = [8, 1, 5, 2, 6]
# a = [8, 8, 8, 8, 0]           # max(A[i] + i), 0 < i < n - 1
# b = [0, 0, 3, -1, 2]          # A[j] - j
# dp = [0, 8, 11, 7, 10]        # max(A[i] + i) + A[j] - j

def maxScoreSightseeingPair(A: List[int]):
    n = len(A)
    a = [0] * n         #
    maxi = 0
    for i in range(n - 1):
        maxi = max(maxi, A[i] + i)
        a[i] = maxi

    dp = [0] + [a[j - 1] + A[j] - j for j in range(1, n)]
    return max(dp)


def main():
    print(maxScoreSightseeingPair([8, 1, 5, 2, 6]))     # 11


if __name__ == "__main__":
    main()
