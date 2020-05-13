#! /usr/local/bin/python3


def hammingWeight(n: int) -> int:
    count, a = 0, 1
    for i in range(32):
        if n & a:
            count += 1
        a <<= 1
    return count


def main():
    print(hammingWeight(int('0b00000000000000000000000000001011', 2)))      # 3
    print(hammingWeight(int('0b00000000000000000000000010000000', 2)))      # 1
    print(hammingWeight(int('0b11111111111111111111111111111101', 2)))      # 31


if __name__ == "__main__":
    main()
