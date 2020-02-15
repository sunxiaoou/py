#! /usr/local/bin/python3


def maximum(array):
    if len(array) == 1:
        return array[0]
    return max(array[0], maximum(array[1:]))


def main():
    print(maximum([8, 6, 17, 14, 3, 32]))


if __name__ == "__main__":
    main()
