#! /usr/local/bin/python3
from time import sleep


def isHappy(n: int) -> bool:
    nums = [n]
    while n != 1:
        res = []
        while n:
            n, r = divmod(n, 10)
            res.append(r)
        n = sum(r * r for r in res)
        print(n)
        if n in nums:
            return False
        nums.append(n)
        # sleep(.1)
    return True


def main():
    print(isHappy(19))          # True
    print(isHappy(77))          # True


if __name__ == "__main__":
    main()
