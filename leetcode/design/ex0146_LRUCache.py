#! /usr/local/bin/python3
from collections import deque
from typing import List


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = deque(maxlen=capacity)
        self.dic = {}

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.remove(key)
        self.cache.append(key)
        return self.dic[key]

    def put(self, key: int, value: int) -> None:
        assert key > 0
        if key not in self.cache:
            self.cache.append(key)
        else:
            self.cache.remove(key)
            self.cache.append(key)
        self.dic[key] = value


def test(data: List[List[int]]) -> List[int]:
    cache = None
    res = []
    for i in range(len(data)):
        if i == 0:
            cache = LRUCache(data[i][0])
            res.append(None)
        elif len(data[i]) == 2:
            cache.put(data[i][0], data[i][1])
            res.append(None)
        elif len(data[i]) == 1:
            res.append(cache.get(data[i][0]))
        # print(cache.cache)
    return res


def main():
    data = [[2], [2,1], [1,1], [2,3], [4,1], [1], [2]]
    res = [None, None, None, None, None, -1, 3]
    print('OK') if test(data) == res else print('KO')
    data = [[2], [2], [2,6], [1], [1,5], [1,2], [1], [2]]
    res = [None, -1, None, -1, None, None, 2, 6]
    print('OK') if test(data) == res else print('KO')
    data = [[2], [1,1], [2,2], [1], [3,3], [2], [3], [4,4], [1], [3], [4]]
    res = [None, None, None, 1, None, -1, 3, None, -1, 3, 4]
    print('OK') if test(data) == res else print('KO')


if __name__ == "__main__":
    main()
