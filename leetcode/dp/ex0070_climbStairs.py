#! /usr/local/bin/python3


def climbStairs(n: int) -> int:
    if n == 1:
        return 1
    if n == 2:
        return 2

    n1, n2, n3 = 1, 2, 3
    for i in range(2, n):
        n3 = n1 + n2
        n1, n2 = n2, n3

    return n3


def main():
    print(climbStairs(5))


if __name__ == "__main__":
    main()
