#! /usr/local/bin/python3


def isPalindrome(s: str) -> bool:
    n = len(s)
    if n == 0:
        return True
    left, right = 0, n - 1
    while left < right:
        if not s[left].isalpha() and not s[left].isdigit():
            left += 1
            continue
        if not s[right].isalpha() and not s[right].isdigit():
            right -= 1
            continue
        if s[left].lower() == s[right].lower():
            left += 1
            right -= 1
        else:
            return False
    return True


def main():
    print(isPalindrome("A man, a plan, a canal: Panama"))       # True
    print(isPalindrome("race a car"))                           # False


if __name__ == "__main__":
    main()
