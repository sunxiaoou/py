#! /usr/local/bin/python3
from typing import List


def topKFrequent(nums: List[int], k: int) -> List[int]:
    dic = {}
    for i in nums:
        if i not in dic:
            dic[i] = 1
        else:
            dic[i] += 1
    return sorted(dic.keys(), key=(lambda x: dic[x]), reverse=True)[: k]


def main():
    print(topKFrequent([1, 1, 1, 2, 2, 3], 2))      # [1, 2]
    print(topKFrequent([1], 1))                     # [1]


if __name__ == "__main__":
    main()
