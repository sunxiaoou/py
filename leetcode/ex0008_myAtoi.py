#! /usr/local/bin/python3
import re


def myAtoi(str: str) -> int:
    regex = re.compile(r' *([+-]?\d+)')
    try:
        s2 = regex.match(str).group(1)
    except AttributeError:
        return 0
    flag = '+'
    if s2[0] == '+' or s2[0] == '-':
        flag = s2[0]
        s2 = s2[1:]
    res = ord(s2[0]) - ord('0')
    for i in range(1, len(s2)):
        res = res * 10 + ord(s2[i]) - ord('0')
    if flag == '-':
        res = -res
    if res < -2147483648:
        res = -2147483648
    elif res > 2147483647:
        res = 2147483647
    return res


def main():
    print(myAtoi(" 42"))     # 42
    print(myAtoi("-42"))    # -42
    print(myAtoi("4193 with words"))    # 4193
    print(myAtoi("words and 987"))      # 0
    print(myAtoi("-91283472332"))       # -2147483648


if __name__ == "__main__":
    main()
