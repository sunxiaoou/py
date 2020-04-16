#! /usr/local/bin/python3
from typing import List


"""
Interval DP

recurrence:
dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j])           # i <= k < j, arr[i] != arr[j]
dp[i][j] = min(dp[i + 1][j - 1], dp[i][k] + dp[k + 1][j])   # i <= k < j, arr[i] == arr[j]

dp[i][j] is the solution for the sub-array from index i to index j.
When arr[i] == arr[j] one transition could be just dp(i + 1, j + 1), because in the last turn
we would have a palindrome and we can extend this palindrome from both sides
"""


def print_dp(arr: List[int], dp: List[List[int]]):
    row0 = ['\\\\'] + [str(i) for i in arr]
    print(', '.join(row0))
    for i in range(len(arr)):
        print("{},  {}".format(str(arr[i]), ', '.join([str(j) if str(j) != 'inf' else '∞' for j in dp[i]])))


def minimumMoves(arr: List[int]) -> int:
    n = len(arr)
    dp = [[float('inf')] * n for _ in range(n)]
    print_dp(arr, dp)
    for j in range(n):
        print('({})'.format(j))
        # i must uses reverse order because dp(i, j) is subset of dp(i - 1, j)
        for i in range(j, -1, -1):                      # i uses reverse order
            print('\t({}, {})'.format(i, j))
            if i == j:                                  # only one integer, one op
                dp[i][j] = 1
            elif i + 1 == j and arr[i] == arr[j]:       # two same integers, is palindrome, one op
                dp[i][j] = 1
            elif i + 1 == j and arr[i] != arr[j]:       # two different integers, two ops
                dp[i][j] = 2
            else:
                for k in range(i, j):                   # minimum of any of 2 parts sum
                    print('\t\t({}, {}, {}) ({}, {}) ({}, {}) ({})'.
                          format(i, j, k, i, k, k + 1, j, dp[i][k] + dp[k + 1][j]))
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j])
                if arr[i] == arr[j]:                    # count subset dp(i + 1, j - 1)
                    dp[i][j] = min(dp[i][j], dp[i + 1][j - 1])
    print_dp(arr, dp)
    return dp[0][-1]


def main():
    # print(minimumMoves([1, 2]))
    # print(minimumMoves([1, 3, 4, 1, 5]))
    print(minimumMoves([1, 4, 1, 1, 2, 1]))


if __name__ == "__main__":
    main()
