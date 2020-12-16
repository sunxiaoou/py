#! /usr/bin/python3


def mod2(a: int) -> int:
    b = i = 0
    while a:
        a, re = divmod(a, 10)
        b += re % 2 * (2 ** i)
        i += 1
    return b


def two_mod2(a: int, b: int) -> bool:
    s = mod2(a + b)
    s2 = mod2(a) + mod2(b)
    if s == s2:
        print(a + b, s, mod2(a), mod2(b), s2)
    return s == s2


def main():
    # print(two_mod2(12, 23))
    # print(two_mod2(97, 23))
    count = 0
    for i in range(10, 100):
        if two_mod2(i, 23):
            count += 1
            print(i)
    print(count)


if __name__ == "__main__":
    main()
