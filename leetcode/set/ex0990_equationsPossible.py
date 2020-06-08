#! /usr/local/bin/python3
from typing import List


def equationsPossible(equations: List[str]) -> bool:
    sets = []
    for eq in sorted(equations, key=(lambda x: x[1]), reverse=True):
        if eq[1: 3] == "==":
            s1 = s2 = None
            for s in sets:
                if eq[0] in s and eq[3] in s:
                    break
                if eq[0] in s:
                    s1 = s
                elif eq[3] in s:
                    s2 = s
            else:
                if s1 is None and s2 is None:
                    sets.append({eq[0], eq[3]})
                elif s1 is None:
                    s2.add(eq[0])
                elif s2 is None:
                    s1.add(eq[3])
                else:
                    s1 |= s2
                    sets.remove(s2)
        else:
            if eq[0] == eq[3]:
                return False
            s1 = s2 = None
            for s in sets:
                if eq[0] in s and eq[3] in s:
                    return False
                if eq[0] in s:
                    s1 = s
                elif eq[3] in s:
                    s2 = s
            else:
                if s1 is None and s2 is None:
                    sets.append({eq[0]})
                    sets.append({eq[3]})
                elif s1 is None:
                    sets.append({eq[0]})
                elif s2 is None:
                    sets.append({eq[3]})
    return True


def main():
    print(equationsPossible(["a!=a"]))                  # False
    print(equationsPossible(["a==b", "b!=a"]))          # False
    print(equationsPossible(["a==b", "b==c", "a==c"]))  # True
    print(equationsPossible(["a==b", "b!=c", "c==a"]))  # False
    print(equationsPossible(["c==c", "b==d", "x!=z"]))  # True


if __name__ == "__main__":
    main()
