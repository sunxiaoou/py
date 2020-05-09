#! /usr/local/bin/python3
from typing import List


def fizzBuzz(n: int) -> List[str]:
    res = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            res.append('FizzBuzz')
        elif i % 3 == 0:
            res.append('Fizz')
        elif i % 5 == 0:
            res.append('Buzz')
        else:
            res.append(str(i))
    return res


def main():
    print(fizzBuzz(15))


if __name__ == "__main__":
    main()
