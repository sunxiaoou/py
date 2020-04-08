#! /usr/local/bin/python3
from typing import List


def gameOfLife(board: List[List[int]]) -> None:
    b2 = []
    n = len(board)
    m = len(board[0])
    for i in range(n):
        row = []
        for j in range(m):
            up = board[i - 1][j] if i > 0 else 0
            down = board[i + 1][j] if i < n - 1 else 0
            left = board[i][j - 1] if j > 0 else 0
            right = board[i][j + 1] if j < m - 1 else 0
            upleft = board[i - 1][j - 1] if i > 0 and j > 0 else 0
            upright = board[i - 1][j + 1] if i > 0 and j < m - 1 else 0
            downleft = board[i + 1][j - 1] if i < n - 1 and j > 0 else 0
            downright = board[i + 1][j + 1] if i < n - 1 and j < m - 1 else 0
            around = up + down + left + right + upleft + upright + downleft + downright

            x = board[i][j]
            if x == 1 and around < 2 or around > 3:
                x = 0
            elif x == 0 and around == 3:
                x = 1
            row.append(x)
        b2.append(row)

    for i in range(n):
        for j in range(m):
            board[i][j] = b2[i][j]


def main():
    board = [[0, 1, 0],           # [0, 0, 0],
             [0, 0, 1],           # [1, 0, 1],
             [1, 1, 1],           # [0, 1, 1],
             [0, 0, 0]]           # [0, 1, 0]
    gameOfLife(board)
    print(board)


if __name__ == "__main__":
    main()
