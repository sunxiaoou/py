#! /usr/local/bin/python3


def reverseBits(n: int) -> int:
    a = 0
    for i in range(32):
        a <<= 1
        a |= n & 1
        n >>= 1
    # print(bin(a))
    return a


def main():
    print(reverseBits(int('0b00000010100101000001111010011100', 2)))    # 964176192
    print(reverseBits(int('0b11111111111111111111111111111101', 2)))    # 3221225471


if __name__ == "__main__":
    main()
