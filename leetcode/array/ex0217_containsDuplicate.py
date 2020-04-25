#! /usr/local/bin/python3
from typing import List


def containsDuplicate(nums: List[int]) -> bool:
    dup = {}
    for i in range(len(nums)):
        if nums[i] not in dup:
            dup[nums[i]] = i
        else:
            return True
    return False


def main():
    print(containsDuplicate([1, 2, 3, 1]))                      # True
    print(containsDuplicate([1, 2, 3, 4]))                      # False
    print(containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))    # True


if __name__ == "__main__":
    main()
