#! /usr/local/bin/python3
from typing import List


def numRookCaptures(board: List[List[str]]) -> int:
    x = y = 0
    for i in range(len(board)):
        try:
            x = board[i].index("R")
        except Exception:
            pass
        else:
            y = i
            break

    count = 0
    for i in range(y - 1, -1, -1):
        if board[i][x] == "p":
            count += 1
            break
        if board[i][x] != ".":
            break

    for i in range(y + 1, len(board)):
        if board[i][x] == "p":
            count += 1
            break
        if board[i][x] != ".":
            break

    for i in range(x - 1, -1, -1):
        if board[y][i] == "p":
            count += 1
            break
        if board[y][i] != ".":
            break

    for i in range(x + 1, len(board[x])):
        if board[y][i] == "p":
            count += 1
            break
        if board[y][i] != ".":
            break

    return count


def main():
    board = [[".",".",".","p",".",".",".","."],
             [".",".",".",".",".",".",".","."],
             [".",".",".","R",".","B",".","p"],
             [".",".",".",".",".",".",".","."],
             [".",".",".",".",".",".",".","."],
             [".",".",".","p",".",".",".","."],
             [".",".",".",".",".",".",".","."],
             [".",".",".",".",".",".",".","."]]

    num = numRookCaptures(board)
    print(num)


if __name__ == "__main__":
    main()
