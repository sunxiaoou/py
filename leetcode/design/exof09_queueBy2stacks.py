#! /usr/local/bin/python3
from typing import List


class CQueue:
    def __init__(self):
        self.stack = []
        self.stack2 = []

    def appendTail(self, value: int) -> None:
        self.stack.append(value)

    def deleteHead(self) -> int:
        if not self.stack2:
            while self.stack:
                self.stack2.append(self.stack.pop())
        if not self.stack2:
            return -1
        return self.stack2.pop()


def test(commands: List[str], args: List[List[int]]) -> List[int]:
    n, obj, res = len(commands), None, [None]
    for i in range(n):
        expr = commands[i] + "(" + ", ".join([str(i) for i in args[i]]) + ")"
        if not i:
            obj = eval(expr)        # eval is an evil creature
        else:
            res.append(eval("obj." + expr))
    return res


def main():
    commands = ["CQueue", "appendTail", "deleteHead", "deleteHead"]
    args = [[], [3], [], []]
    print(test(commands, args))       # [None, None, 3, -1]

    commands = ["CQueue", "deleteHead", "appendTail", "appendTail", "deleteHead", "deleteHead"]
    args = [[], [], [5], [2], [], []]
    print(test(commands, args))         # [None, -1, None, None, 5, 2]


if __name__ == "__main__":
    main()
