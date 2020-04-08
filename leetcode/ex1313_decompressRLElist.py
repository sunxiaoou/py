#! /usr/local/bin/python3
from typing import List


def decompressRLElist(nums: List[int]) -> List[int]:
    result = []
    count = 0
    for i in range(len(nums)):
        if i % 2 == 0:
            count = nums[i]
        else:
            result += [nums[i]] * count
    return result


def main():
    resutl = decompressRLElist([1, 2, 3, 4])
    resutl = decompressRLElist([1, 1, 2, 3])
    print(resutl)


if __name__ == "__main__":
    main()
