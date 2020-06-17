#! /usr/local/bin/python3


def fractionToDecimal(numerator: int, denominator: int) -> str:
    if not numerator:
        return "0"
    is_negative = False
    if numerator < 0 and denominator < 0:
        numerator, denominator = -numerator, -denominator
    elif numerator < 0:
        numerator = -numerator
        is_negative = True
    elif denominator < 0:
        denominator = -denominator
        is_negative = True

    qu, re = divmod(numerator, denominator)
    s = str(qu)
    if not re:
        return s if not is_negative else "-" + s
    s2 = ""
    res = []
    while re and re not in res:
        res.append(re)
        re *= 10
        qu, re = divmod(re, denominator)
        s2 += str(qu)
    if re:
        i = res.index(re)
        s2 = s2[: i] + "(" + s2[i:] + ")"
    return s + "." + s2 if not is_negative else "-" + s + "." + s2


def main():
    print(fractionToDecimal(0, -5))             # "0"
    print(fractionToDecimal(-2147483648, 1))    # "-2147483648"
    print(fractionToDecimal(-50, 8))            # "-6.25"
    print(fractionToDecimal(1, 6))              # "0.1(6)"
    print(fractionToDecimal(19, 27))            # "0.(703)"
    print(fractionToDecimal(2, 3))              # "0.(6)"
    print(fractionToDecimal(1, 2))              # "0.5"
    print(fractionToDecimal(2, 1))              # "2"


if __name__ == "__main__":
    main()
