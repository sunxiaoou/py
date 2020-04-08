#! /usr/local/bin/python3
from functools import reduce
from operator import mul


def fact(n):
    return reduce(mul, range(1, n + 1))


def numWays(n: int) -> int:
    n1 = n
    n2 = 0
    result = 0
    while n1 >= 0:
        # print(n1, n2)
        if n1 == 0 or n2 == 0:
            result += 1
        else:
            result += fact(n - n2) // fact(n1) // fact(n2)
        n1 -= 2
        n2 += 1
    return result % 1000000007


def main():
    print(numWays(2))
    print(numWays(44))
    print(numWays(7))


if __name__ == "__main__":
    main()
