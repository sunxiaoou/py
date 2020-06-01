#! /usr/local/bin/python3
from typing import List


def kidsWithCandies(candies: List[int], extraCandies: int) -> List[bool]:
    maxi = max(candies)
    return [True if i + extraCandies >= maxi else False for i in candies]


def main():
    print(kidsWithCandies([2, 3, 5, 1, 3], 3))      # [True, True, True, False, True]
    print(kidsWithCandies([4, 2, 1, 1, 2], 1))      # [True, False, False, False, False]
    print(kidsWithCandies([12, 1, 12], 10))         # [True, False, True]


if __name__ == "__main__":
    main()
