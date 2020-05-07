#! /usr/local/bin/python3
from random import randint
from typing import List


class Solution:
    def __init__(self, nums: List[int]):
        self.nums = nums[:]
        self.backup = nums[:]

    def reset(self) -> List[int]:
        """
        Resets the array to its original configuration and return it.
        """
        self.nums[:] = self.backup[:]
        return self.nums

    def shuffle(self) -> List[int]:
        """
        Returns a random shuffling of the array.
        """
        n = len(self.nums)
        for i in range(n):
            j = randint(0, n - 1)
            self.nums[i], self.nums[j] = self.nums[j], self.nums[i]
        return self.nums


def main():
    obj = Solution([1, 2, 3])
    print(obj.reset())
    print(obj.shuffle())


if __name__ == "__main__":
    main()
