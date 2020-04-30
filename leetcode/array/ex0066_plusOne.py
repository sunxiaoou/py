#! /usr/local/bin/python3
from typing import List


def plusOne(digits: List[int]) -> List[int]:
    n = len(digits)
    carry = 1
    for i in range(n - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += carry
            carry = 0
            break
        else:
            digits[i] = 0
            carry = 1
    if carry:
        return [1] + digits
    return digits


def main():
    print(plusOne([1, 2, 3]))           # [1, 2, 4]
    print(plusOne([9, 9, 9]))           # [1, 0, 0, 0]
    pass


if __name__ == "__main__":
    main()
