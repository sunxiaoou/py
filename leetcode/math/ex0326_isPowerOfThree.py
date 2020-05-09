#! /usr/local/bin/python3


def isPowerOfThree(n: int) -> bool:
    i = 1
    while i < n:
        i *= 3
    if i == n:
        return True
    return False


def main():
    print(isPowerOfThree(27))       # True
    print(isPowerOfThree(0))        # False
    print(isPowerOfThree(9))        # True


if __name__ == "__main__":
    main()
