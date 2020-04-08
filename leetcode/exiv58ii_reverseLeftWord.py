#! /usr/local/bin/python3


def reverseLeftWords(s: str, n: int) -> str:
    return s[n:] + s[:n]


def main():
    s = reverseLeftWords("abcdefg", 2)
    s = reverseLeftWords("lrloseumgh",  6)
    print(s)


if __name__ == "__main__":
    main()
