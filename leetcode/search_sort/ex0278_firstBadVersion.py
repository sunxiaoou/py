#! /usr/local/bin/python3


def isBadVersion(version: int) -> bool:
    return False if version < 4 else True


def firstBadVersion(n: int) -> int:
    left, right, count = 0, n - 1, 0
    while left <= right:
        mid = (left + right) // 2
        if isBadVersion(mid):
            right = mid - 1
        else:
            left = mid + 1
        count += 1
    print(count)
    return left


def main():
    print(firstBadVersion(65))       # 4


if __name__ == "__main__":
    main()
