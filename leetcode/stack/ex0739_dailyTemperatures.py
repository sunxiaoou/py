#! /usr/local/bin/python3
from typing import List


def dailyTemperatures_slow(T: List[int]) -> List[int]:
    n = len(T)
    nums = [0] * n
    for i in range(n):
        for j in range(i, n):
            if T[i] < T[j]:
                nums[i] = j - i
                break
    return nums


# monotonic stack
def dailyTemperatures(T: List[int]) -> List[int]:
    n = len(T)
    res = [0] * n
    stack = []
    for i in range(n):
        while stack and T[stack[-1]] < T[i]:
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return res


def main():
    print(dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]))
    # [1, 1, 4, 2, 1, 1, 0, 0]


if __name__ == "__main__":
    main()
