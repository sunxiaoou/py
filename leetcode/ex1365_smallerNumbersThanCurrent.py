#! /usr/local/bin/python3
from typing import List


def smallerNumbersThanCurrent(nums: List[int]) -> List[int]:
    s = sorted(nums)
    return [s.index(i) for i in nums]


def main():
    x = smallerNumbersThanCurrent([8, 1, 2, 2, 3])
    x = smallerNumbersThanCurrent([6, 5, 4, 8])
    x = smallerNumbersThanCurrent([7, 7, 7, 7])
    print(x)


if __name__ == "__main__":
    main()
