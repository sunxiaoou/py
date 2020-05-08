#! /usr/local/bin/python3


def mySqrt_slow(x: int) -> int:
    a = 1
    while a * a <= x:
        a += 1
    return a - 1


def mySqrt(x: int) -> int:
    left, right = 0, x
    while left <= right:
        mid = (left + right) // 2
        m2 = mid * mid
        print(left, mid, right, (mid - 1) * (mid - 1), m2, (mid + 1) * (mid + 1))
        if m2 == x:
            return mid
        if (mid - 1) * (mid - 1) < x < m2:
            return mid - 1
        if m2 < x:
            left = mid + 1
        else:
            right = mid - 1
    return 0


def main():
    print(mySqrt(6))        # 2
    print(mySqrt(4))        # 2
    print(mySqrt(10))       # 3


if __name__ == "__main__":
    main()
