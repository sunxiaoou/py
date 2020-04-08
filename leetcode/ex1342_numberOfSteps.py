#! /usr/local/bin/python3


def numberOfSteps(num: int) -> int:
    if num == 0:
        return 0

    if num % 2 == 0:
        num /= 2
    else:
        num -= 1
    return 1 + numberOfSteps(num)


def main():
    n = numberOfSteps(14)
    n = numberOfSteps(123)
    n = numberOfSteps(8)
    print(n)


if __name__ == "__main__":
    main()
