#! /usr/local/bin/python3
from typing import List


def generate(numRows: int) -> List[List[int]]:
    if not numRows:
        return []

    res = [[1]]
    for i in range(1, numRows):
        row = [1]
        for j in range(1, i + 1):
            if j == len(res[i - 1]):
                a = 1
            else:
                a = res[i - 1][j - 1] + res[i - 1][j]
            row.append(a)
        res.append(row)
    return res


def main():
    print(generate(5))      # [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]


if __name__ == "__main__":
    main()
