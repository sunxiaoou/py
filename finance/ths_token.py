#! /usr/bin/python3

import pyperclip


def main():
    header = 'Cookie: '
    cookie = pyperclip.paste()
    assert cookie.startswith(header), print(cookie[: len(header)])
    f = open('auth/ths_cookie.txt', 'w')
    f.write(cookie.lstrip(header))
    f.close()


if __name__ == "__main__":
    main()
