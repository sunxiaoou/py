#! /usr/local/bin/python3
import re


def defangIPaddr(address: str) -> str:
    regex = re.compile(r'\.')
    return regex.sub('[.]', address)


def main():
    result = defangIPaddr("1.1.1.1")
    result = defangIPaddr("255.100.50.0")
    print(result)


if __name__ == "__main__":
    main()
