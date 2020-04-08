#! /usr/local/bin/python3
from typing import List


def findNumbers(nums: List[int]) -> int:
    return sum(len(str(i)) % 2 == 0 for i in nums)


def main():
    result = findNumbers([12, 345, 2, 6, 7896])
    result = findNumbers([555, 901, 482, 1771])
    print(result)


if __name__ == "__main__":
    main()
