#! /usr/local/bin/python3


def lengthOfLongestSubstring2(s: str) -> int:
    n, dictionary = len(s), {}
    i = j = res = 0                 # j points to substring beginning
    for i in range(n):
        if s[i] in dictionary and j <= dictionary[s[i]]:
            res = max(res, i - j)
            j = dictionary[s[i]] + 1
        dictionary[s[i]] = i
        # print(dictionary, (i, j), res)
    return max(res, i + 1 - j)      # i += 1 because last i in for loop is n - 1


def lengthOfLongestSubstring(s: str) -> int:
    if not s:
        return 0
    n, dic = len(s), {}
    dp = [0] * n                    # dp[i] is length of current substring
    j = 0                           # j points to current substring beginning
    for i in range(n):
        if s[i] in dic and dic[s[i]] >= j:  # dup char before j doesn't impact current substring
            j = dic[s[i]] + 1               # update j to next to dup char
        dic[s[i]] = i
        dp[i] = i - j + 1
    # print(dp)
    return max(dp)


def main():
    print(lengthOfLongestSubstring("abc"))          # 3
    print(lengthOfLongestSubstring("abcabcbb"))     # 3
    print(lengthOfLongestSubstring("bbbbb"))        # 1
    print(lengthOfLongestSubstring("pwwkewp"))      # 4
    pass


if __name__ == "__main__":
    main()
