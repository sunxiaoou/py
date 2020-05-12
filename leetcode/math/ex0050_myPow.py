#! /usr/local/bin/python3


def myPow_slow(x: float, n: int) -> float:
    if x == 0:
        return 0
    if n == 0:
        return 1
    if n < 0:
        x = 1 / x
        n = -n
    res = x
    for i in range(n - 1):
        res *= x
    return res


def myPow_slow2(x: float, n: int) -> float:
    if x == 0:
        return 0
    if n == 0:
        return 1
    if n < 0:
        x = 1 / x
        n = -n

    def power(n: int) -> float:
        nonlocal x
        if n == 1:
            return x
        m, r = divmod(n, 2)
        print(m)
        if not r:
            return power(m) * power(m)
        else:
            return power(m) * power(m) * x

    return power(n)


def myPow(x: float, n: int) -> float:
    if n == 0:
        return 1
    if n < 0:
        n = -n
        x = 1 / x
    i = 0
    dp = []                 # dynamic program
    while n > 0:
        dp.append(n & 1)    # append flag    1 ->  0 ->  1 -> 1 -> 0 -> 0 -> 1
        n >>= 1             # divide power  77 -> 38 -> 19 -> 9 -> 4 -> 2 -> 1
        i += 1
    dp = dp[:: -1]          # calculate     77 <- 38 <- 19 <- 9 -> 4 <- 2 <- 1
    dp[0] = x
    for i in range(1, len(dp)):
        if dp[i] == 0:
            dp[i] = dp[i - 1] * dp[i - 1]
        else:
            dp[i] = dp[i - 1] * dp[i - 1] * x
    return dp[-1]


def main():
    print(myPow(1.2, 77))               # 1250132.21181
    print(myPow(0.00001, 2147483647))   # 0.25000
    print(myPow(2.00000, 10))           # 1024.00000
    print(myPow(2.10000, 3))            # 9.26100
    print(myPow(2.00000, -2))           # 0.25000


if __name__ == "__main__":
    main()
