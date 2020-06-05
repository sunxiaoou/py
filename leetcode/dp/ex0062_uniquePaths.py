#! /usr/local/bin/python3


def uniquePaths_slow(m: int, n: int) -> int:
    count = 0

    def backtrack(i: int, j: int):
        nonlocal count
        # print(i, j)
        if i == n - 1 and j == m - 1:
            count += 1
            return
        if i + 1 < n:
            i += 1
            backtrack(i, j)
            i -= 1
        if j + 1 < m:
            j += 1
            backtrack(i, j)
            j -= 1

    backtrack(0, 0)
    return count


def uniquePaths(m: int, n: int) -> int:
    dp = [[1] * m for _ in range(n)]
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[-1][-1]


def main():
    print(uniquePaths(3, 2))        # 3
    print(uniquePaths(7, 3))        # 28
    print(uniquePaths(18, 18))      # 2333606220
    print(uniquePaths(23, 12))      # 193536720


if __name__ == "__main__":
    main()
