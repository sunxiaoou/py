#! /usr/local/bin/python3


def isNumber(s: str) -> bool:
    try:
        float(s)
    except Exception:
        return False
    return True


def main():
    print(isNumber("+100"))
    print(isNumber("+5e2"))
    print(isNumber("-123"))
    print(isNumber("3.1416"))
    print(isNumber("0123"))
    print(isNumber("-1E-16"))

    print(isNumber("12e"))
    print(isNumber("1a3.14"))
    print(isNumber("1.2.3"))
    print(isNumber("+-5"))
    print(isNumber("12e+5.4"))


if __name__ == "__main__":
    main()
