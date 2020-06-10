#! /usr/local/bin/python3
from random import randint, choice
from typing import List


class RandomizedSetSlow:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.rands = set()

    def insert(self, val: int) -> bool:
        """
        Inserts a value to the set. Returns True if the set did not already contain the specified element.
        """
        if val in self.rands:
            return False
        self.rands.add(val)
        return True

    def remove(self, val: int) -> bool:
        """
        Removes a value from the set. Returns True if the set contained the specified element.
        """
        if val not in self.rands:
            return False
        self.rands.remove(val)
        return True

    def getRandom(self) -> int:
        """
        Get a random element from the set.
        """
        return list(self.rands)[randint(0, len(self.rands) - 1)]


class RandomizedSet:
    def __init__(self):
        self.arr = []
        self.dic = {}

    def insert(self, val: int) -> bool:
        if val in self.dic:
            return False
        self.arr.append(val)
        self.dic[val] = len(self.arr) - 1
        return True

    def remove(self, val: int) -> bool:
        if val not in self.dic:
            return False
        i = self.dic[val]
        self.dic[self.arr[-1]] = i          # dic, set index of last element to i
        self.dic.pop(val)                   # remove index from dic, maybe only one
        self.arr[i] = self.arr[-1]          # arr, move last element to i
        self.arr.pop()                      # remove last element
        return True                         # so it is O(1) time

    def getRandom(self) -> int:
        return choice(self.arr)


def test(comms: List[str], paras: List[List[int]]) -> List[int]:
    obj = None
    res = []
    for i in range(len(comms)):
        if comms[i] == "RandomizedSet":
            obj = RandomizedSet()
            res.append(None)
        elif comms[i] == "insert":
            res.append(obj.insert(paras[i][0]))
        elif comms[i] == "remove":
            res.append(obj.remove(paras[i][0]))
        elif comms[i] == "getRandom":
            res.append(obj.getRandom())
    return res


def main():
    commands = ["RandomizedSet", "remove", "remove", "insert", "getRandom", "remove", "insert"]
    parameters = [[], [0], [0], [0], [], [0], [0]]
    print(test(commands, parameters))       # [null,false,false,true,0,true,true]
    commands = ["RandomizedSet", "insert", "insert", "remove", "insert", "remove", "getRandom"]
    parameters = [[], [0], [1], [0], [2], [1], []]
    print(test(commands, parameters))       # [null,true,true,true,true,true,2]
    commands = ["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
    parameters = [[], [1], [2], [2], [], [1], [2], []]
    print(test(commands, parameters))       # [null,true,false,true,1,true,false,2]


if __name__ == "__main__":
    main()
