#! /usr/local/bin/python3
from typing import List


def loops(m: int, n: int):
    res = []

    def backtrack(ans: List[int]):
        if len(ans) == n:
            res.append(ans[:])
            return
        for i in range(m):
            ans.append(i)
            backtrack(ans)
            ans.pop()

    backtrack([])
    print(len(res))
    for i in res:
        print(i)


def main():
    loops(2, 3)


if __name__ == "__main__":
    main()
