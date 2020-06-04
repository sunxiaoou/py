#! /usr/local/bin/python3


def sumNums(n: int) -> int:
    return n and n + sumNums(n - 1)


def main():
    print(sumNums(6))   # 21


if __name__ == "__main__":
    main()
