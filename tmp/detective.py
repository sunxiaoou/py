#! /usr/local/bin/python3
from typing import List

"""
2018年刑侦科推理试题 单项选择，（每题10分，共100分）

1. 这道题的答案是：
    A.A B.B C.C D.D

2. 第5髓的答案是；
    A.C B.D C.A D.B

3. 以下选项中哪一题的签案与其他三项不同；
    A.第3题 B.第6姬 C.第2题 D.第4题

4. 以下选项中哪两题的答案相同：
    A.第1,5题 B.第2,7题 C.第1,9题 D.第6,10题

5. 以下选项中哪一题的答案与本题相同：
    A.第8题 B.第4题 C.第9题 D.第7题

6. 以下选项中感两题的答案与第8题相问：
    A.第2,4题 B.第1,6题 C.第3,10题 D.第5,9题

7. 在此十道题中，被选中次数最少的选项字母为：
    A.C B.B C.A D.D

8. 以下选项中哪一题的答案与第1题的答案在字母中不相邻
    A.第7题 B.第5题 C.第2题 D.第10题

9. 已知“第1题与第6题的答案相同”与“第X题与第5题的答案相间”的真假性相反，那么X为：
    A.第6题 B.第10题 C.第2题 D.第9题

10. 在此10道题中，ABCD四个字母出现次数最多与最少者的差为：
    A.3 B.2 C.4 D.1
"""


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
    ans = [-1]                  # -1 is a placeholder, as answer begins with index 1
    backtrack()
    ans = [chr(ans[i] + ord('A')) for i in range(1, n + 1)]
    print(ans)


if __name__ == "__main__":
    main()

