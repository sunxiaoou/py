#! /usr/local/bin/python3
from typing import List


class UnionFind:
    def __init__(self, capacity: int):
        self.parent = list(range(capacity))                     # [i for i in range(capacity)]

    def find(self, ind: int) -> int:
        while ind != self.parent[ind]:
            self.parent[ind] = self.parent[self.parent[ind]]    # compress tree optimization
            ind = self.parent[ind]
        return ind

    def union(self, ind1: int, ind2: int):
        self.parent[self.find(ind1)] = self.find(ind2)          # merge ind1 into ind2


def equationsPossible(equations: List[str]) -> bool:
    uf = UnionFind(26)
    for st in equations:
        if st[1] == "=":
            index1 = ord(st[0]) - ord("a")
            index2 = ord(st[3]) - ord("a")
            uf.union(index1, index2)
    for st in equations:
        if st[1] == "!":
            index1 = ord(st[0]) - ord("a")
            index2 = ord(st[3]) - ord("a")
            if uf.find(index1) == uf.find(index2):
                return False
    return True


def main():
    print(equationsPossible(["a!=a"]))                  # False
    print(equationsPossible(["a==b", "b!=a"]))          # False
    print(equationsPossible(["a==b", "b==c", "a==c"]))  # True
    print(equationsPossible(["a==b", "b!=c", "c==a"]))  # False
    print(equationsPossible(["c==c", "b==d", "x!=z"]))  # True


if __name__ == "__main__":
    main()
