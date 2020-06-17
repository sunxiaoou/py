#! /usr/local/bin/python3


def divide_slow(dividend: int, divisor: int) -> int:
    is_negative = False
    if dividend < 0 and divisor < 0:
        dividend, divisor = -dividend, -divisor
    elif dividend < 0:
        dividend = -dividend
        is_negative = True
    elif divisor < 0:
        divisor = -divisor
        is_negative = True

    count = su = 0
    while True:
        su += divisor
        if su > dividend:
            break
        count += 1

    return count if not is_negative else -count


def d2(dividend: int, divisor: int) -> int:
    count, su = 1, divisor
    while su + su < dividend:
        su += su
        count += count
    re = dividend - su
    if re < divisor:
        return count
    return count + d2(dividend - su, divisor)


def divide(dividend: int, divisor: int) -> int:
    if abs(dividend) < abs(divisor):
        return 0

    if divisor == 1:
        return dividend
    if divisor == -1:
        return -dividend if dividend > -2147483648 else 2147483647

    is_negative = False
    if dividend < 0 and divisor < 0:
        dividend, divisor = -dividend, -divisor
    elif dividend < 0:
        dividend = -dividend
        is_negative = True
    elif divisor < 0:
        divisor = -divisor
        is_negative = True
    count = d2(dividend, divisor)
    return count if not is_negative else -count


def main():
    print(divide(-2147483648, 1))       # 1
    print(divide(-2147483648, -1))      # 1
    print(divide(11, 3))                # 3
    print(divide(1, 1))                 # 1
    print(divide(7, -3))                # -2


if __name__ == "__main__":
    main()
