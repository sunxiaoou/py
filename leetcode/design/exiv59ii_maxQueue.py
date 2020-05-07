#! /usr/local/bin/python3
from collections import deque


class MaxQueue:
    def __init__(self):
        self.dq = deque(maxlen=10000)

    def max_value(self) -> int:
        if len(self.dq) == 0:
            return -1
        return max(i for i in self.dq)

    def push_back(self, value: int) -> None:
        self.dq.append(value)

    def pop_front(self) -> int:
        if len(self.dq) == 0:
            return -1
        return self.dq.popleft()


def main():
    obj = MaxQueue()
    obj.push_back(2)
    obj.push_back(0)
    obj.push_back(100)
    print(obj.max_value())
    print(obj.pop_front())
    print(obj.pop_front())


if __name__ == "__main__":
    main()
