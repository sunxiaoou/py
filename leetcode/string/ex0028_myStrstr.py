#! /usr/local/bin/python3


def strStr(haystack: str, needle: str) -> int:
    n1, n2 = len(haystack), len(needle)
    i, j, same = 0, 0, False
    while i < n1 and j < n2:
        if not same:
            if haystack[i] == needle[j]:
                i += 1
                j += 1
                same = True
            else:
                i += 1
        else:
            if haystack[i] == needle[j]:
                i += 1
                j += 1
            else:
                i -= j - 1          # cannot use i += 1 here, maybe there is overlap
                j = 0
                same = False
    if j == n2:
        return i - n2
    return -1


def main():
    print(strStr("mississippi", "issip"))   # 4
    print(strStr("hello", "ll"))            # 2
    print(strStr("hello", "o"))             # 4
    print(strStr("hello", ""))              # 0
    print(strStr("aaaaa", "bba"))           # -1

    pass


if __name__ == "__main__":
    main()
