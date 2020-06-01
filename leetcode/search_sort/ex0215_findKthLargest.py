#! /usr/local/bin/python3
from typing import List


def findKthLargest(nums: List[int], k: int) -> int:
    return sorted(nums, reverse=True)[k - 1]


def main():
    print(findKthLargest([3,2,1,5,6,4], 2))         # 5
    print(findKthLargest([3,2,3,1,2,4,5,5,6], 4))   # 4


if __name__ == "__main__":
    main()
