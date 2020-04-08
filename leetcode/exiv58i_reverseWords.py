#! /usr/local/bin/python3


def reverseWords(s: str) -> str:
    words = s.split()
    return " ".join(words[:: -1])


def main():
    print(reverseWords("the sky is blue"))
    print(reverseWords("  hello world!  "))
    print(reverseWords("a good   example"))


if __name__ == "__main__":
    main()
