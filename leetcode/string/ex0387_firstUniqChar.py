#! /usr/local/bin/python3


def firstUniqChar(s: str) -> int:
    n, d = len(s), {}
    if n == 0:
        return -1
    for i in range(n):
        if s[i] in d:
            d[s[i]] = n         # set a big value as a duplicate flag
        else:
            d[s[i]] = i

    res = min(i for i in d.values())
    return res if res < n else -1


def main():
    print(firstUniqChar("leetcode"))        # 0
    print(firstUniqChar("loveleetcode"))    # 2


if __name__ == "__main__":
    main()
