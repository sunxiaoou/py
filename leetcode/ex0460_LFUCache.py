#! /usr/local/bin/python3
from typing import List
from bisect import bisect_left, insort


class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.time = 0
        self.history = []   # node - (count, time, key)
        self.lfu = {}       # entry - key: [value, count, time]

    def get(self, key: int) -> int:
        if key not in self.lfu:
            return -1
        self.time += 1
        value, count, time = self.lfu[key]
        entry = self.lfu[key]
        entry[1] += 1                                       # update entry, entry[1] is count
        position = bisect_left(self.history, (count, time, key))
        self.history.pop(position)
        insort(self.history, (count + 1, self.time, key))   # update node
        return value

    def put(self, key: int, value: int) -> None:
        if not self.capacity:
            return
        self.time += 1
        if key in self.lfu:
            _, count, time = self.lfu[key]
            # self.lfu[key][0] = value
            # self.lfu[key][1] = count + 1
            # self.lfu[key][2] = self.time
            self.lfu[key][:] = value, count + 1, self.time      # update entry, [:] means local assignment
            position = bisect_left(self.history, (count, time, key))
            self.history.pop(position)
            insort(self.history, (count + 1, self.time, key))   # update node
            return
        if len(self.lfu) == self.capacity:
            node = self.history.pop(0)              # remove first node
            self.lfu.pop(node[2])                   # remove relevant entry, node[2] is key
        self.lfu[key] = [value, 1, self.time]       # insert entry
        insort(self.history, (1, self.time, key))   # insert node


def test(data: List[List[int]]) -> List[int]:
    cache = None
    res = []
    for i in range(len(data)):
        if i == 0:
            cache = LFUCache(data[i][0])
            res.append(None)
        elif len(data[i]) == 2:
            cache.put(data[i][0], data[i][1])
            res.append(None)
        elif len(data[i]) == 1:
            res.append(cache.get(data[i][0]))
        # print(cache.queue)
    return res


def main():
    data = [[2], [1,1], [2,2], [1], [3,3], [2], [3], [4,4], [1], [3], [4]]
    res = [None, None, None, 1, None, -1, 3, None, -1, 3, 4]
    print('OK') if test(data) == res else print('KO')

    data = [[3], [2, 2], [1, 1], [2], [1], [2], [3,3], [4,4], [3], [2], [1], [4]]
    res = [None, None, None, 2, 1, 2, None, None, -1, 2, 1, 4]
    print('OK') if test(data) == res else print('KO')

    data = [[2], [3,1], [2,1], [2,2], [4,4], [2]]
    res = [None, None, None, None, None, 2]
    print('OK') if test(data) == res else print('KO')

    data = [[0], [0, 0], [0]]
    res = [None, None, -1]
    print('OK') if test(data) == res else print('KO')

    data = [[3],[1,1],[2,2],[3,3],[4,4],[4],[3],[2],[1],[5,5],[1],[2],[3],[4],[5]]
    res = [None, None, None, None, None, 4, 3, 2, -1, None, -1, 2, 3, -1, 5]
    print('OK') if test(data) == res else print('KO')
    # print(test(commands, data))


if __name__ == "__main__":
    main()
