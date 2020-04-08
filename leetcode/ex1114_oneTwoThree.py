#! /usr/local/bin/python3
from concurrent import futures
from queue import Queue
from typing import Callable, List


class Foo:
    def __init__(self):
        self.q1 = Queue()
        self.q2 = Queue()
        self.res = Queue()

    def printFirst(self):
        self.res.put('one')

    def printSecond(self):
        self.res.put('two')

    def printThird(self):
        self.res.put('three')

    def first(self, printFirst: 'Callable[[], None]') -> None:
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.q1.put(1)

    def second(self, printSecond: 'Callable[[], None]') -> None:
        self.q1.get()
        # printFirst() outputs "first". Do not change or remove this line.
        printSecond()
        self.q2.put(1)

    def third(self, printThird: 'Callable[[], None]') -> None:
        self.q2.get()
        # printThird() outputs "third". Do not change or remove this line.
        printThird()


def oneTwoThree(nums: List[int]) -> str:
    foo = Foo()
    funcs = [(foo.first, foo.printFirst), (foo.second, foo.printSecond), (foo.third, foo.printThird)]

    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        todo = []
        for n in nums:
            future = executor.submit(funcs[n - 1][0], funcs[n - 1][1])
            todo.append(future)

        for future in futures.as_completed(todo):
            future.result()

    res = ''
    while not foo.res.empty():
        res += foo.res.get()
    return res


def main():
    print(oneTwoThree([1, 2, 3]))
    print(oneTwoThree([3, 2, 1]))


if __name__ == "__main__":
    main()
