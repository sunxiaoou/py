#! /usr/local/bin/python3
from typing import List

"""
[1]                     # push 1, 2, 3 in order at first level
[1, 2]                  # push 2, 3 in order at second level
[1, 2, 3]               # push 3 in third level
[1, 2, 3]               # got one answer, pop 3 from 3rd
[1, 2]                  # no more at 3rd, return and pop 2 from 2nd
[1, 3]                  # 3 is next item at 2nd, push it in 
[1, 3, 2]               # push 2 in 3rd
[1, 3, 2]               # got one answer, pop 2 from 3rd
[1, 3]                  # no more at 3rd, return and pop 3 from 2nd
[1]                     # no more at 2rd, return and pop 1 from ist
[2]                     # 2 is next item at 1st, push it in
[2, 1]                  # ...
[2, 1, 3]
[2, 1, 3]
[2, 1]
[2, 3]
[2, 3, 1]
[2, 3, 1]
[2, 3]
[2]
[3]
[3, 1]
[3, 1, 2]
[3, 1, 2]
[3, 1]
[3, 2]
[3, 2, 1]
[3, 2, 1]
[3, 2]
[3]
"""


def permute(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    if n == 0:
        return []
    used = [False] * n
    res = []

    def backtrack(ans: List[int]):
        if len(ans) == n:
            res.append(ans[:])
            return

        for i in range(n):
            if not used[i]:
                used[i] = True
                ans.append(nums[i])
                # print(ans)
                backtrack(ans)
                used[i] = False
                # print(ans)
                ans.pop()

    backtrack([])
    # print(len(res))

    return res


def main():
    print(permute([1]))
    print(permute([1, 2, 3]))
    # [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]


if __name__ == "__main__":
    main()
