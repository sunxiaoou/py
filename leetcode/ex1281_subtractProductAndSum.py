#! /usr/local/bin/python3
from functools import reduce
from operator import mul


def subtractProductAndSum(n: int) -> int:
    s = sum(ord(c) - ord('0') for c in str(n))
    p = reduce(mul, [ord(c) - ord('0') for c in str(n)])
    return p - s


def main():
    result = subtractProductAndSum(234)
    result = subtractProductAndSum(4421)
    print(result)


if __name__ == "__main__":
    main()
