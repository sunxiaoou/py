#! /usr/local/bin/python3


def numJewelsInStones(jewels: str, stones: str) -> int:
    num = 0
    for j in jewels:
        num += sum(j == s for s in stones)
    return num


def main():
    result = numJewelsInStones("aA", "aAAbbbb")
    result = numJewelsInStones("z", "ZZ")
    print(result)


if __name__ == "__main__":
    main()
