#! /usr/local/bin/python3


def validPalindrome2(s: str) -> bool:
    n = len(s)
    le, ri = 0, n - 1
    l2 = -1
    one_deleted = False             # has trump card used
    while le < ri:
        if s[le] != s[ri]:
            if one_deleted:
                if l2 == -1:        # no keeping status
                    return False
                le = l2                 # restore status
                # print(s[n - 1 - le])
                ri = n - 1 - le - 1     # and then try from right
                l2 = -1
                continue
            # print(le, s[le], s[le + 1], ri, s[ri - 1], s[ri])
            # if both branch left and right are OK, keep current status, try from left at first
            if s[le + 1] == s[ri] and s[le] == s[ri - 1]:
                l2 = le
            if s[le + 1] == s[ri]:
                # print(s[le])
                le += 1
                one_deleted = True
            elif s[le] == s[ri - 1]:
                # print(s[ri])
                ri -= 1
                one_deleted = True
            else:
                return False
        le += 1
        ri -= 1
    return True


def validPalindrome(s: str) -> bool:

    def is_palindrome(s: str) -> bool:
        n = len(s)
        i, j = 0, n - 1
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    n = len(s)
    i, j = 0, n - 1
    while i < j:
        if s[i] != s[j]:
            break
        i += 1
        j -= 1
    else:
        return True

    if s[i + 1] == s[j] and is_palindrome(s[i + 2: j]):
        return True
    if s[i] == s[j - 1] and is_palindrome(s[i + 1: j - 1]):
        return True
    return False


def main():
    print(validPalindrome("cupucu"))            # True
    print(validPalindrome("aabac"))             # False
    print(validPalindrome("abca"))              # True


if __name__ == "__main__":
    main()
