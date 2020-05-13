#! /usr/local/bin/python3


def hammingDistance(x: int, y: int) -> int:
    n = x ^ y
    count, a = 0, 1
    for i in range(32):
        if n & a:
            count += 1
        a <<= 1
    return count


def main():
    print(hammingDistance(1, 4))    # 2


if __name__ == "__main__":
    main()
