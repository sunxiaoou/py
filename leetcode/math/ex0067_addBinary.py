#! /usr/local/bin/python3


def str2num(a: str) -> int:
    n = len(a)
    j = num = 0
    for i in range(n - 1, -1, -1):
        if a[i] == '1':
            num += 2 ** j
        j += 1
    return num


def addBinary(a: str, b: str) -> str:
    num = str2num(a) + str2num(b)
    if not num:
        return "0"
    res = ""
    while num:
        num, re = divmod(num, 2)
        res = ("1" if re else "0") + res
    return res


def main():
    print(addBinary("0",  "0"))         # 100
    print(addBinary("11",  "1"))        # 100
    print(addBinary("1010", "1011"))    # 10101


if __name__ == "__main__":
    main()
