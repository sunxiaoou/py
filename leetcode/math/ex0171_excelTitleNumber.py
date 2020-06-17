#! /usr/local/bin/python3


def titleToNumber(s: str) -> int:
    res = 0
    for ch in s:
        i = ord(ch) - ord('A') + 1
        res = res * 26 + i
    return res


def main():
    print(titleToNumber("A"))       # 1
    print(titleToNumber("AB"))      # 28
    print(titleToNumber("ZY"))      # 701


if __name__ == "__main__":
    main()
