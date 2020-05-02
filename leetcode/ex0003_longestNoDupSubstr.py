#! /usr/local/bin/python3


def lengthOfLongestSubstring2(s: str) -> int:
    n, dictionary = len(s), {}
    i = j = res = 0
    while i < n:
        if s[i] not in dictionary or dictionary[s[i]] < j:
            dictionary[s[i]] = i
        else:
            res = max(res, i - j)
            j = dictionary[s[i]] + 1
            dictionary[s[i]] = i
        i += 1
        print(dictionary, (i, j), res)
    return max(res, i - j)


def lengthOfLongestSubstring(s: str) -> int:
    n, dictionary = len(s), {}
    i = j = res = 0                 # j points to substring beginning
    for i in range(n):
        if s[i] in dictionary and j <= dictionary[s[i]]:
            res = max(res, i - j)
            j = dictionary[s[i]] + 1
        dictionary[s[i]] = i
        # print(dictionary, (i, j), res)
    return max(res, i + 1 - j)      # i += 1 because last i in for loop is n - 1


def main():
    print(lengthOfLongestSubstring("abc"))          # 3
    print(lengthOfLongestSubstring("abcabcbb"))     # 3
    print(lengthOfLongestSubstring("bbbbb"))        # 1
    print(lengthOfLongestSubstring("pwwkewp"))      # 4
    pass


if __name__ == "__main__":
    main()
