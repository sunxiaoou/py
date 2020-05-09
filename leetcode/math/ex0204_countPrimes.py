#! /usr/local/bin/python3


def countPrimes_slow(n: int) -> int:

    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        if x == 2 or x == 3:
            return True
        i = 2
        while i * i <= x:
            if x % i == 0:
                return False
            i += 1
        return True

    count = 0
    res = []
    for i in range(2, n):
        if is_prime(i):
            # res.append(i)
            count += 1
    # return count
    return count


# create a table, mark all composite numbers off, as each composite is multiple of a prime
def countPrimes(n: int) -> int:
    is_primes = [False, False] + [True] * (n - 2)
    i = 2
    while i * i <= n:
        if is_primes[i]:
            for j in range(i + i, n, i):
                is_primes[j] = False        # mark all multiple of i off
        i = i + 1
    # print(is_primes)
    return is_primes.count(True)


def main():
    print(countPrimes(2))                   # 0
    print(countPrimes(10))                  # 4
    # print(countPrimes_slow(1500000))      # 114155
    print(countPrimes(1500000))             # 114155


if __name__ == "__main__":
    main()
