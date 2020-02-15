#! /usr/local/bin/python3


def length(array):
    if not array:
        return 0
    return 1 + length(array[1:])


def main():
    print(length([0, 1, 2, 3, 4, 5, 6]))


if __name__ == "__main__":
    main()
