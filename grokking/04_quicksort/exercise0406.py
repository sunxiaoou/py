#! /usr/local/bin/python3


def qsort(a):
    if len(a) < 2:
        return a

    a0 = a[0]
    lesser = [i for i in a[1:] if i < a0]
    greater = [i for i in a[1:] if i > a0]
    return qsort(lesser) + [a0] + qsort(greater)


def main():
    print(qsort([10, 5, 89, 3, 42, 7]))


if __name__ == "__main__":
    main()
