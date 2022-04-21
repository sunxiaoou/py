#! /usr/bin/python3
import json
import pprint
import re
import sys

import pyperclip


def main():
    if len(sys.argv) < 2:
        s = pyperclip.paste()
        s = re.sub('\n', '', s)
        pprint.pprint((json.loads(s)))
    else:
        with open(sys.argv[1]) as f:
            lines = f.readlines()
            for i in range(len(lines)):
                line = re.sub('\n', '', lines[i])
                print(i)
                pprint.pprint((json.loads(line)))


if __name__ == "__main__":
    main()
