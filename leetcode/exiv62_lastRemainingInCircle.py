#! /usr/local/bin/python3


def lastRemaining(n: int, m: int) -> int:
    arr = [i for i in range(n)]
    e = None
    i = 0
    while arr:
        i = (i + m - 1) % len(arr)
        e = arr.pop(i)
        print(e)
    return e


def main():
    print(lastRemaining(5, 3))  # 2, 0, 4, 1, 3
    print(lastRemaining(10, 17))


if __name__ == "__main__":
    main()
