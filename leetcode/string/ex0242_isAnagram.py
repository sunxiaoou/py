#! /usr/local/bin/python3


def isAnagram(s: str, t: str) -> bool:
    a = [s[i] for i in range(len(s))]
    b = [t[i] for i in range(len(t))]
    return sorted(a) == sorted(b)


def main():
    print(isAnagram("anagram", "nagaram"))      # True
    print(isAnagram("rat", "car"))              # False


if __name__ == "__main__":
    main()
