#! /usr/local/bin/python3


def split(length, width):
    if length < width:
        length, width = width, length

    mod = length % width
    if mod == 0:
        return width
    else:
        return split(width, mod)


def main():
    print(split(640, 1680))


if __name__ == "__main__":
    main()
