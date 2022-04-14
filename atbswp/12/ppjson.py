#! /usr/bin/python3
import json
import pprint
import re

import pyperclip


def ppjson():
    s = pyperclip.paste()
    s = re.sub('\n', '', s)
    pprint.pprint(json.loads(s))


def main():
    ppjson()


if __name__ == "__main__":
    main()
