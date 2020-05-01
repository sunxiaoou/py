#! /usr/local/bin/python3
import re


def myAtoi(str: str) -> int:
    regex = re.compile(r' *([+-]?\d+)')
    try:
        s = regex.match(str).group(1)
    except AttributeError:
        return 0
    flag = '+'
    if s[0] == '+' or s[0] == '-':
        flag = s[0]
        s = s[1:]
    res = 0
    for i in range(len(s)):
        res = res * 10 + int(s[i])
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
