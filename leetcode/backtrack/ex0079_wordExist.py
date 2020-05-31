#! /usr/local/bin/python3
from typing import List


def exist(board: List[List[str]], word: str) -> bool:
    m, n = len(board[0]), len(board)
    used = [[False] * m for _ in range(n)]
    directions = [(-1, 0), (1, 0), [0, -1], [0, 1]]

    def backtrack(i: int, j: int, k: int):
        if k == len(word):
            return True
        used[i][j] = True
        for y, x in directions:
            i1 = i + y if 0 <= i + y < n else i
            j1 = j + x if 0 <= j + x < m else j
            if board[i1][j1] == word[k] and not used[i1][j1] and backtrack(i1, j1, k + 1):
                return True
        used[i][j] = False          # reset for next search
        return False

    for i in range(n):
        for j in range(m):
            if board[i][j] == word[0] and backtrack(i, j, 1):
                return True
    return False


def main():
    board = [["C", "A", "A"],
             ["A", "A", "A"],
             ["B", "C", "D"]]
    print(exist(board, "AAB"))          # True

    board = [['A', 'B', 'C', 'E'],
             ['S', 'F', 'C', 'S'],
             ['A', 'D', 'E', 'E']]
    print(exist(board, "ABCCED"))       # True
    print(exist(board, "SEE"))          # True
    print(exist(board, "ABCB"))         # False


if __name__ == "__main__":
    main()
