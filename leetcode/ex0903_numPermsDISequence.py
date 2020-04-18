#! /usr/local/bin/python3
from typing import List


def print_dp(di: str, dp: List[List[int]]):
    print('"{}"'.format(di))
    n1, n2 = len(dp), len(dp[0])
    row0 = ['\\\\'] + [str(i) for i in range(n2)]
    print(', '.join(row0))
    for i in range(n1):
        print("{},  {}".format(i, ', '.join([str(j) for j in dp[i]])))


"""
# https://www.cnblogs.com/grandyang/p/11094525.html
dp[i][j] represents total number of permutations in range(0, i) and last number is j

recurrence:
if S[i - 1] == 'D'    dp[i][k] += dp[i - 1][k]    (0 <= k <= j)
else                  dp[i][k] += dp[i - 1][k]    (j < k <= i)

1. "D"
\\, 0, 1            # Decrease, range is (0, i=1), only permutation is (1, j=0)
0,  0, 0            # last number (j) is 0
1,  1, 0            # dp[i][j] = 1

2. "DI"
\\, 0, 1, 2         # Increase, range is (0, 1, i=2), follows [1, j=0]
0,  0, 0, 0         # previous last number (j) is 0, k should be [1, 2],
1,  1, 0, 0         # dp[2][1] = 1, dp[2][2] = 1
2,  0, 1, 1

3. "DID"
\\, 0, 1, 2, 3      # Decrease, range is (0, 1, 2, i=3)
0,  0, 0, 0, 0      # follows (2, 0, j=1) and (1, 0, j=2)
1,  1, 0, 0, 0      # j == 1, k = [0, 1]: dp[3][0] = 1, dp[3][1] = 1
2,  0, 1, 1, 0      # j == 2, k = [0, 1, 2]:
3,  2, 2, 1, 0      # dp[3][0] = 2, dp[3][1] = 2, dp[3][2] = 1

4. "DIDD"
\\, 0, 1, 2, 3, 4   # Decrease, range is (0, 1, 2, 3, i=4)
0,  0, 0, 0, 0, 0   # follows j (0) * 2, (1) * 2 and (2)
1,  1, 0, 0, 0, 0   # j == 0, k = [0],  dp[4][0] = 2
2,  0, 1, 1, 0, 0   # j == 1, k = [0, 1], dp[4][0] = 4, dp[4][1] = 2
3,  2, 2, 1, 0, 0   # j == 2, k = [0, 1, 2], dp[4][0] = 5, dp[4][1] = 3, dp[4][2] = 1
4,  5, 3, 1, 0, 0
"""


def numPermsDISequence(S: str) -> int:
    n = len(S) + 1
    dp = [[0] * n for _ in range(n)]
    # print_dp(S, dp)

    if S[0] == 'D':
        dp[1][0] = 1
    else:
        dp[1][1] = 1

    for i in range(2, n):
        for j in range(n - 1):
            if dp[i - 1][j] > 0:
                if S[i - 1] == 'D':
                    for k in range(j + 1):
                        dp[i][k] += dp[i - 1][j]
                else:
                    for k in range(j + 1, i + 1):
                        dp[i][k] += dp[i - 1][j]
    print_dp(S, dp)
    return sum(i for i in dp[-1]) % 1000000007


def main():
    print(numPermsDISequence("D"))                          # 1
    print(numPermsDISequence("DI"))                         # 2
    print(numPermsDISequence("DID"))                        # 5
    print(numPermsDISequence("DIDD"))                       # 9
    print(numPermsDISequence("IDDDIIDIIIIIIIIDIDID"))       # 853197538


if __name__ == "__main__":
    main()
