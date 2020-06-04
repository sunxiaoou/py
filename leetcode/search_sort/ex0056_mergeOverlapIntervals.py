#! /usr/local/bin/python3
from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    n = len(intervals)
    intervals.sort()
    res = []
    le, ri = intervals[0]
    for i in range(1, n):
        if ri >= intervals[i][0]:
            ri = max(ri, intervals[i][1])
        else:
            res.append([le, ri])
            le, ri = intervals[i]
    res.append([le, ri])
    return res


def main():
    print(merge([[1, 4], [4, 5]]))                      # [[1,5]]
    print(merge([[1, 3], [2, 6], [8, 10], [15, 18]]))   # [[1,6],[8,10],[15,18]]


if __name__ == "__main__":
    main()
