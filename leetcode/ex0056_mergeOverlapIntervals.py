#! /usr/local/bin/python3
from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    n = len(intervals)
    if n < 2:
        return intervals

    intervals.sort()
    result = []
    i = 0
    while True:
        if i == n - 1:
            result.append(intervals[i])
            break
        a0, a1 = intervals[i]
        b0, b1 = intervals[i + 1]
        if a1 < b0:
            result.append(intervals[i])
        else:
            intervals[i + 1] = [a0, max(a1, b1)]
        i += 1
    return result


def main():
    print(merge([[1, 4], [4, 5]]))                      # [[1,6],[8,10],[15,18]]
    print(merge([[1, 3], [2, 6], [8, 10], [15, 18]]))  # [[1,5]]


if __name__ == "__main__":
    main()
