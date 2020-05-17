#! /usr/local/bin/python3


def longestPalindrome(s: str) -> str:
    n = len(s)
    sr = s[:: -1]
    dp = [[0] * n for _ in range(n)]
    maxi = ''
    for i in range(n):
        for j in range(n):
            if sr[i] != s[j]:
                dp[i][j] = 0
            else:
                if i and j:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = 1    # first row or first column
                if dp[i][j] > len(maxi):
                    tmp = s[j - dp[i][j] + 1: j + 1]    # maybe answer candidate
                    if tmp == tmp[:: -1]:               # is it palindrome?
                        maxi = tmp
    return maxi


def main():
    print(longestPalindrome("aaaabbba"))    # abbba
    print(longestPalindrome("abcdba"))      # a or b or c or d
    print(longestPalindrome("ac"))          # a or c
    print(longestPalindrome("babad"))       # bab or aba
    print(longestPalindrome("cbbd"))        # bb


if __name__ == "__main__":
    main()
