#! /usr/local/bin/python3


def isMatch2(s: str, p: str) -> bool:
    if not p:
        return not s
    first_match = len(s) > 0 and p[0] in {s[0], '.'}
    if len(p) > 1 and p[1] == "*":
        return isMatch(s, p[2:]) or (first_match and isMatch(s[1:], p))
    return first_match and isMatch(s[1:], p[1:])


# dp[i][j] represents s[: i] matches p[: j] or not
def isMatch(s: str, p: str) -> bool:
    s, p = " " + s, " " + p                         # add placeholders, " " represent ""
    m, n = len(s), len(p)
    dp = [[False] * n for _ in range(m)]
    dp[0][0] = True                                 # "" matches ""
    for j in range(1, n):                           # set first line
        if p[j] == "*":                             # "" matches "a*" something
            dp[0][j] = dp[0][j - 2]
    # print(dp[0])
    for i in range(1, m):
        for j in range(n):
            if p[j] in {s[i], "."}:
                dp[i][j] = dp[i - 1][j - 1]         # match 1 time
            elif p[j] == "*":
                if p[j - 1] in {s[i], "."}:
                    dp[i][j] = dp[i - 1][j] or dp[i][j - 2]     # match 0, 1 or multiple time(s)
                else:
                    dp[i][j] = dp[i][j - 2]         # match 0 time
        # print(dp[i])
    return dp[-1][-1]


def main():
    print(isMatch("aab", "c*a*b"))                  # True
    #    "", c, *, a, *, b
    # "" [T, F, T, F, T, F]                         # Ts: "" = "", "" = "c*", "" = "c*a*"
    # a  [F, F, F, T, T, F]                         # Ts: "a" = "c*a", "a" = "c*a*"
    # a  [F, F, F, F, T, F]                         # Ts: "aa" = "c*a*"
    # b  [F, F, F, F, F, T]                         # Ts: "aab" = "c*a*b"
    print(isMatch("ab", "a."))                      # True
    print(isMatch("aa", "a*"))                      # True
    print(isMatch("aaa", "a*a"))                    # True
    print(isMatch("aa", "a"))                       # False
    print(isMatch("ab", ".*"))                      # True
    print(isMatch("mississippi", "mis*is*p*."))     # False


if __name__ == "__main__":
    main()
