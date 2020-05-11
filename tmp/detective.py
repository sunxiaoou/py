#! /usr/local/bin/python3
from typing import List


def check(a: List) -> bool:
    c2 = [a[2] == 0 and a[5] == 2,
          a[2] == 1 and a[5] == 3,
          a[2] == 2 and a[5] == 0,
          a[2] == 3 and a[5] == 1].count(True) == 1

    c3 = [a[3] == 0 and a[3] != a[6] == a[2] == a[4],
          a[3] == 1 and a[6] != a[3] == a[2] == a[4],
          a[3] == 2 and a[2] != a[3] == a[6] == a[4],
          a[3] == 3 and a[4] != a[3] == a[6] == a[2]].count(True) == 1

    c4 = [a[4] == 0 and a[1] == a[5],
          a[4] == 1 and a[2] == a[7],
          a[4] == 2 and a[1] == a[9],
          a[4] == 3 and a[6] == a[10]].count(True) == 1

    c5 = [a[5] == 0 == a[8],
          a[5] == 1 == a[4],
          a[5] == 2 == a[9],
          a[5] == 3 == a[7]].count(True) == 1

    c6 = [a[6] == 0 and a[8] == a[2] == a[4],
          a[6] == 1 and a[8] == a[1] == a[6],
          a[6] == 2 and a[8] == a[3] == a[10],
          a[6] == 3 and a[8] == a[5] == a[9]].count(True) == 1

    counts = {0: 0, 1: 0, 2: 0, 3: 0}
    for i in a[1:]:
        counts[i] += 1
    minkey = min(counts.keys(), key=(lambda k: counts[k]))
    maxkey = max(counts.keys(), key=(lambda k: counts[k]))

    c7 = [a[7] == 0 and minkey == 2,
          a[7] == 1 and minkey == 1,
          a[7] == 2 and minkey == 0,
          a[7] == 3 and minkey == 3].count(True) == 1

    c8 = [a[8] == 0 and abs(a[1] - a[7]) > 1,
          a[8] == 1 and abs(a[1] - a[5]) > 1,
          a[8] == 2 and abs(a[1] - a[2]) > 1,
          a[8] == 3 and abs(a[1] - a[10]) > 1].count(True) == 1

    def s1d3(t: int, k: int, n: List[int]) -> bool:
        return t == n[k] and n.count(t) == 1

    def d1s3(t: int, k: int, n: List[int]) -> bool:
        return t != n[k] and n.count(t) == 3

    nums = [a[6], a[10], a[2], a[9]]
    c91 = [a[9] == 0 and s1d3(a[5], 0, nums),
           a[9] == 1 and s1d3(a[5], 1, nums),
           a[9] == 2 and s1d3(a[5], 2, nums),
           a[9] == 3 and s1d3(a[5], 3, nums)].count(True) == 1
    c92 = [a[9] == 0 and d1s3(a[5], 0, nums),
           a[9] == 1 and d1s3(a[5], 1, nums),
           a[9] == 2 and d1s3(a[5], 2, nums),
           a[9] == 3 and d1s3(a[5], 3, nums)].count(True) == 1
    c9 = (a[1] != a[6] and c91) or (a[1] == a[6] and c92)

    diff = counts[maxkey] - counts[minkey]
    c10 = [a[10] == 0 and diff == 3,
           a[10] == 1 and diff == 2,
           a[10] == 2 and diff == 4,
           a[10] == 3 and diff == 1].count(True) == 1

    if c2 and c3 and c4 and c5 and c6 and c7 and c8 and c9 and c10:
        return True
    return False


def main():

    def backtrack():            # generate each permutation of answers
        if len(ans) == n + 1:
            if check(ans):
                return True
            return False
        for i in range(m):
            ans.append(i)
            if backtrack():
                return True
            ans.pop()

    m, n = 4, 10
    ans = [-1]                  # -1 is a placeholder, as answer begin with index 1
    backtrack()
    ans = [chr(ans[i] + ord('A')) for i in range(1, n + 1)]
    print(ans)


if __name__ == "__main__":
    main()
