#! /usr/local/bin/python3


def romanToInt(s: str) -> int:
    romans = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000,
              'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
    n = len(s)
    res = i = 0
    while i < n - 1:
        b = s[i] == 'I' and (s[i + 1] == 'V' or s[i + 1] == 'X')
        b = b or (s[i] == 'X' and (s[i + 1] == 'L' or s[i + 1] == 'C'))
        b = b or (s[i] == 'C' and (s[i + 1] == 'D' or s[i + 1] == 'M'))
        if b:
            res += romans[s[i] + s[i + 1]]
            i += 2
        else:
            res += romans[s[i]]
            i += 1
    if i < n:
        res += romans[s[i]]
    return res


def main():
    print(romanToInt("III"))        # 3
    print(romanToInt("IV"))         # 4
    print(romanToInt("IX"))         # 9
    print(romanToInt("LVIII"))      # 58
    print(romanToInt("MCMXCIV"))    # 1994


if __name__ == "__main__":
    main()
