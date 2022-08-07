#! /usr/bin/python3
import sys

import pyperclip


def clipboard2file(file: str):
    text = pyperclip.paste()
    # if file.endswith('_cookie.txt'):
    #     header = 'Cookie: '
    #     assert text.startswith(header), print(text[: len(header)])
    #     text = text.lstrip(header)
    with open(file, 'w') as fp:
        fp.write(text)


def main():
    if len(sys.argv) < 2:
        print('Usage: {} txt'.format(sys.argv[0]))
        sys.exit(1)

    clipboard2file(sys.argv[1])


if __name__ == "__main__":
    main()
