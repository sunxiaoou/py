#! /usr/local/bin/python3
from typing import List


def game(guess: List[int], answer: List[int]) -> int:
    return sum(a == b for a, b in zip(guess, answer))


def main():
    n = game([1, 2, 3], [1, 2, 3])
    n = game([2, 2, 3], [3, 2, 1])
    print(n)


if __name__ == "__main__":
    main()
