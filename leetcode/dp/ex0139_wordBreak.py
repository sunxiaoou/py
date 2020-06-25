#! /usr/local/bin/python3
from typing import List


# dp[i] represents s[0: i] is matched or not
def wordBreak(s: str, wordDict: List[str]) -> bool:
    s = " " + s                         # add placeholder
    n = len(s)
    dp = [True] + [False] * (n - 1)     # suppose empty string is matched
    for i in range(1, n):
        for j in range(i):              # enumerate each j in (0, i - 1)
            if dp[j] and s[j + 1: i + 1] in wordDict:
                dp[i] = True
                break
    # print(dp)
    return dp[-1]


def main():
    print(wordBreak("leetcode", ["leet", "code"]))                          # True
    print(wordBreak("applepenapple", ["apple", "pen"]))                     # True
    print(wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]))    # False
    # [T, F, F, T, T, F, F, T, F, F]    4T matched "", "cat", "cats" and "catsand"


if __name__ == "__main__":
    main()
