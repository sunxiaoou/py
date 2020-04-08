#! /usr/local/bin/python3
from typing import List


def spiralOrder(matrix: List[List[int]]) -> List[int]:
    b = len(matrix) - 1
    if b < 0:
        return []
    a = len(matrix[0]) - 1

    direction = 0
    i = j = 0
    result = []
    while True:
        if matrix[i][j] is None:
            break
        result.append(matrix[i][j])
        # print(result)
        matrix[i][j] = None
        if direction == 0:  # right
            if j < a and matrix[i][j + 1] is not None:
                j += 1
            elif i < b:
                direction = 1
                i += 1
            else:
                break
        elif direction == 1:    # down
            if i < b and matrix[i + 1][j] is not None:
                i += 1
            elif j > 0:
                direction = 2
                j -= 1
            else:
                break
        elif direction == 2:    # left
            if j > 0 and matrix[i][j - 1] is not None:
                j -= 1
            elif i > 0:
                direction = 3
                i -= 1
            else:
                break
        elif direction == 3:    # up
            if i > 0 and matrix[i - 1][j] is not None:
                i -= 1
            elif j < a:
                direction = 0
                j += 1
            else:
                break
    return result


def main():

    print(spiralOrder([]))
    print(spiralOrder([[1]]))

    print(spiralOrder([[1, 2],
                      [3, 4]]))

    print(spiralOrder([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9]]))

    print(spiralOrder([[1, 2, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 11, 12]]))


if __name__ == "__main__":
    main()
