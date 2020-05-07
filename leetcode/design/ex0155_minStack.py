#! /usr/local/bin/python3


class MinStack:
    def __init__(self):
        """
        initialize your data structure here.
        """
        self.nums = []
        self.minimum = 0

    def push(self, x: int) -> None:
        self.nums.append(x)
        self.minimum = min(self.nums)

    def pop(self) -> None:
        self.nums.pop()
        if self.nums:
            self.minimum = min(self.nums)

    def top(self) -> int:
        return self.nums[-1]

    def getMin(self) -> int:
        return self.minimum


def main():
    obj = MinStack()
    obj.push(-2)
    obj.push(0)
    obj.push(-3)
    print(obj.getMin())     # -3
    obj.pop();
    print(obj.top())        # 0
    print(obj.getMin())     # -2


if __name__ == "__main__":
    main()
