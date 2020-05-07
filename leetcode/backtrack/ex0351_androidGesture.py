#! /usr/local/bin/python3
from typing import List


def gesture(start: int, num: int) -> int:
    panel = [0] * 9                 # 0 1 2
    # result = []                   # 3 4 5
    count = 0                       # 6 7 8

    def backtrack(ans: List[int], curr: int):
        if len(ans) == num:
            # result.append([i for i in ans])
            nonlocal count
            count += 1
            return
        subsequents = []
        for i in range(9):             # search possible cells for next step
            # knight moves or adjacent cells (in a row or in a column), as (0, 1) (0, 5)
            cond1 = (curr + i) % 2
            average = (curr + i) // 2
            # adjacent cells on diagonal, as (0, 4) (1, 3)
            cond2 = curr % 2 == i % 2 and average != 4 and (curr % 2 == 1 or (curr == 4 or i == 4))
            # two cells skip cell 4 between them, as (0, 8), 4 must be used
            cond3 = curr % 2 == i % 2 and average == 4
            cond3 = cond3 and panel[average] == 1
            # two cells on end of same row or column, as (0, 2), average must be used
            cond4 = curr % 2 == 0 and curr != 4 and i % 2 == 0 and i != 4 and\
                abs(curr - i) % 4 != 0
            cond4 = cond4 and panel[average] == 1
            if not panel[i] and (cond1 or cond2 or cond3 or cond4):
                subsequents.append(i)
        for i in subsequents:
            panel[i] = 1                # set the cell used
            ans.append(i)               # add the cell to answer
            backtrack(ans, i)           # enter next level
            ans.pop()                   # pop the cell
            panel[i] = 0                # unset the cell, so it can be used in other answer
        # else:
        #   print('Not found')

    panel[start] = 1                    # set first cell used
    backtrack([start], start)           # add it to answer
    # return result
    return count


def numberOfPatterns(m: int, n: int) -> int:
    if not 0 < m <= n <= 9:
        return 0
    count = 0
    for i in range(m, n + 1):
        count += gesture(0, i) * 4 + gesture(1, i) * 4 + gesture(4, i)
    return count


def main():
    # print(android_gesture(0, 2))
    print(numberOfPatterns(1, 1))
    print(numberOfPatterns(2, 2))
    print(numberOfPatterns(3, 3))
    print(numberOfPatterns(4, 4))
    print(numberOfPatterns(5, 5))
    print(numberOfPatterns(6, 6))
    print(numberOfPatterns(7, 7))
    print(numberOfPatterns(8, 8))
    print(numberOfPatterns(9, 9))
    print(numberOfPatterns(1, 9))


def test():
    pairs = []
    for i in range(9):
        for j in range(9):
            if j > i:
                pairs.append((i, j))
    # print(len(pairs))
    # print(pairs)

    result = []                # test condition2
    for i, j in pairs:
        average = (j + i) // 2
        if j % 2 == i % 2 and average != 4 and (j % 2 == 1 or (j == 4 or i == 4)):
            result.append((i, j))
    print(len(result))
    print(result)

    result = []                 # test condition3
    for i, j in pairs:
        average = (j + i) // 2
        if j % 2 == i % 2 and average == 4:
            result.append((i, j))
    print(len(result))
    print(result)               # [(0, 8), (1, 7), (2, 6), (3, 5)]

    result = []                 # test condition4
    for i, j in pairs:
        if j % 2 == 0 and j != 4 and i % 2 == 0 and i != 4 and abs(j - i) % 4 != 0:
            result.append((i, j))
    print(len(result))
    print(result)               # [(0, 2), (0, 6), (2, 8), (6, 8)]


if __name__ == "__main__":
    # test()
    main()
