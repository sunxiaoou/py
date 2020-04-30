#! /usr/local/bin/python3
from typing import List


def isValidSudoku(board: List[List[str]]) -> bool:
    n = 9
    for i in range(n):
        tmp = []
        for j in range(n):
            if board[i][j] in tmp:
                print(i, j, board[i][j])
                return False
            if board[i][j] != '.':
                tmp.append(board[i][j])

    for j in range(n):
        tmp = []
        for i in range(n):
            if board[i][j] in tmp:
                print(i, j, board[i][j])
                return False
            if board[i][j] != '.':
                tmp.append(board[i][j])

    for i in range(3):
        for j in range(3):
            tmp = []
            for k in range(i * 3, (i + 1) * 3):
                for l in range(j * 3, (j + 1) * 3):
                    if board[k][l] in tmp:
                        print(k, l, board[k][l])
                        return False
                    if board[k][l] != '.':
                        tmp.append(board[k][l])
    return True


def main():
    soduku = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
    
    soduku = [
        ["8", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        [".", "8", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
    
    print(isValidSudoku(soduku))


if __name__ == "__main__":
    main()
