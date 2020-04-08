#! /usr/local/bin/python3
from typing import List


def createTargetArray(nums: List[int], index: List[int]) -> List[int]:
    result = []
    for n, i in zip(nums, index):
        result.insert(i, n)
    return result


def main():
    result = createTargetArray([0, 1, 2, 3, 4], [0, 1, 2, 2, 1])
    # result = createTargetArray([1, 2, 3, 4, 0], [0, 1, 2, 3, 0])
    print(result)


if __name__ == "__main__":
    main()
