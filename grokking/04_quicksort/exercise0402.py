#! /usr/local/bin/python3


def add(a):
    if len(a) == 0:
        return 0
    return a[0] + add(a[1:])


def main():
    print(add([1, 2, 3, 4, 5]))


if __name__ == "__main__":
    main()
