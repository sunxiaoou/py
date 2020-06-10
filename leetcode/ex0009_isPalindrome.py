#! /usr/local/bin/python3


def isPalindrome(x: int) -> bool:
    s = str(x)
    i, j = 0, len(s) - 1
    while i < j and s[i] == s[j]:
        i += 1
        j -= 1
    if i < j:
        return False
    return True


def main():
    print(isPalindrome(121))        # True
    print(isPalindrome(-121))       # False
    print(isPalindrome(10))         # False


if __name__ == "__main__":
    main()
