#! /usr/local/bin/python3
from typing import List


def oddBeforeEven(nums: List[int]) -> List[int]:
    odds = [n for n in nums if n % 2 == 1]
    evens = [n for n in nums if n % 2 == 0]
    return odds + evens


def main():
    print(oddBeforeEven([1, 2, 3, 4]))


if __name__ == "__main__":
    main()
