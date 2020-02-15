#! /usr/local/bin/python3


def search(e, array):
    if not array:
        return None
    if len(array) == 1:
        return 0 if e == array[0] else None

    mid = len(array) // 2
    if e == array[mid]:
        return mid
    if e < array[mid]:
        return search(e, array[: mid])
    i = search(e, array[mid:])
    return None if i is None else mid + i


def main():
    print(search(13, [1, 3, 5, 7, 9, 11]))


if __name__ == "__main__":
    main()
