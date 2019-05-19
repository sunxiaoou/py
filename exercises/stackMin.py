#! /usr/local/bin/python3


class StackMin:
    def __init__(self):
        self.stack = []
        self.len = 0
        self.min = 0

    def push(self, x):
        self.stack.append(x)
        if self.stack[self.min] > x:
            self.min = self.len
        self.len += 1

    def pop(self):
        if self.len == 0:
            return None
        self.len -= 1
        return self.stack[self.len]

    def peak_min(self):
        if self.len == 0:
            return None
        return self.stack[self.min]

    def __str__(self):
        return str(self.stack[:self.len])


def main():
    stack = StackMin()
    for i in [3, 2, 1, 4, 3]:
        stack.push(i)
        print(stack)

    print("min: {}".format(stack.peak_min()))

    while True:
        x = stack.pop()
        if x is None:
            break
        print("{}: {}".format(x, stack))


if __name__ == "__main__":
    main()
