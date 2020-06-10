#! /usr/local/bin/python3
from functools import reduce


def trailingZeroes_slow(n: int) -> int:
    n = reduce(lambda a, b: a * b, range(1, n + 1))
    count = 0
    while n:
        n, re = divmod(n, 10)
        if re:
            break
        count += 1
    return count


# count = n / 5 + n / 5 ^ 2 + n / 5 ^ 3 + ...
def trailingZeroes(n: int) -> int:
    count = 0
    while n:
        n //= 5
        count += n
    return count


def main():
    print(trailingZeroes(7))        # 1
    print(trailingZeroes(11))       # 2
    print(trailingZeroes(30))       # 7


if __name__ == "__main__":
    main()
