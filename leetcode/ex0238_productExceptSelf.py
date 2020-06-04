#! /usr/local/bin/python3
from typing import List


# Can we calculate product of entire array and, div it by each number?
# No, because there is a zero among them maybe
def productExceptSelf(nums: List[int]) -> List[int]:
    n = len(nums)
    pl = [1] * n                # left product array
    for i in range(1, n):
        pl[i] = pl[i - 1] * nums[i - 1]
    pr = [1] * n                # right product array
    for i in range(n - 2, -1, -1):
        pr[i] = pr[i + 1] * nums[i + 1]
    print(pl, pr)
    return [a * b for a, b in zip(pl, pr)]


def main():
    print(productExceptSelf([2, 3, 4, 5]))          # [[60, 40, 30, 24]
    print(productExceptSelf([1, 0, 3, 4]))          # [0, 12, 0, 0]


if __name__ == "__main__":
    main()
