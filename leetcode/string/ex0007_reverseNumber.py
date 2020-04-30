#! /usr/local/bin/python3


def reverseNumber(x: int) -> int:
    positive = True if x >= 0 else False
    x, y = abs(x), 0
    while x:
        x, r = divmod(x, 10)
        y = y * 10 + r

    if positive:
        return y if y < 2 ** 31 - 1 else 0
    return -y if -y > -2 ** 31 else 0


def main():
    print(reverseNumber(123))           # 321
    print(reverseNumber(-123))          # -321
    print(reverseNumber(120))           # 21
    print(reverseNumber(1534236469))    # 0



if __name__ == "__main__":
    main()
