#! /usr/local/bin/python3


def isMatch(s: str, p: str) -> bool:
    s, p = " " + s, " " + p
    m, n = len(s), len(p)
    dp = [[False] * n for _ in range(m)]
    dp[0][0] = True
    for j in range(1, n):
        if p[j] == "*":
            dp[0][j] = dp[0][j - 1]
    print(dp[0])
    for i in range(1, m):
        for j in range(1, n):
            if p[j] in [s[i], "?"]:                         # match 1 time
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j] == "*":
                # because new s[i] matches "*", dp[i][j] == dp[i - 1][j]
                # because new "*" matches s[i], dp[i][j] == dp[i][j - 1]
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
        print(dp[i])

    return dp[-1][-1]


def main():
    print(isMatch("adceb", "*a*b"))         # True
    """
       ""  *  a  *  b      
    "" [T, T, F, F, F]                      # "" == "", "" == "*" 
    a  [F, T, T, T, F]                      # "a" == "*" == "*a" == "*a*"
    d  [F, T, F, T, F]                      # "ad" == "*" == "*a*"
    c  [F, T, F, T, F]                      # "adc" == "*" == "*a*"    
    e  [F, T, F, T, F]                      # "adce" == "*" == "*a*"
    b  [F, T, F, T, T]                      # "adceb" == "*" == "*a*" == "*a*b"
    """

    print(isMatch("aa", "a"))               # False
    print(isMatch("aa", "*"))               # True
    print(isMatch("ab", "?a"))              # False
    print(isMatch("acdcb", "a*c?b"))        # False


if __name__ == "__main__":
    main()
