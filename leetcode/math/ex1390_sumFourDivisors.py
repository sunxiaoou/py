#! /usr/local/bin/python3
from functools import reduce
from itertools import product
from typing import List


def get_primes(n) -> List[int]:
    is_primes = [False, False] + [True] * (n - 2)
    i = 2
    while i * i < n:
        if is_primes[i]:
            for j in range(i + i, n, i):
                is_primes[j] = False
        i += 1
    return [i for i in range(n) if is_primes[i]]


def get_divisors(n: int, primes: List[int]) -> int:
    i = 0
    pds = {}            # primes divisors
    while n > 1:
        qu, re = divmod(n, primes[i])
        if re:
            i += 1
        else:
            if primes[i] not in pds:
                pds[primes[i]] = 1
            else:
                pds[primes[i]] += 1
            n = qu
    # print(pds)
    if sum(pds.values()) + len(pds) != 4:
        return 0

    lis = []
    for k, v in pds.items():
        a, b = [1], k
        for i in range(v):
            a.append(b)
            b *= k
        lis.append(a[:])
    # print(lis)

    divisors = reduce(lambda l1, l2: [a * b for a, b in product(l1, l2)], lis)
    return sum(divisors)


def sumFourDivisors(nums: List[int]) -> int:
    primes = get_primes(max(nums) + 1)
    # print(primes)
    summary = 0
    for n in nums:
        summary += get_divisors(n, primes)
    return summary


def main():
    print(sumFourDivisors([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))     # 45
    print(sumFourDivisors([5]))                                 # 0
    print(sumFourDivisors([21, 4, 7, 60]))                      # 32


if __name__ == "__main__":
    main()
