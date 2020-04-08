#! /usr/local/bin/python3
from collections import deque
from concurrent import futures
from threading import Lock
from time import sleep
from typing import Callable

NUM = 5


class DiningPhilosophers:
    def __init__(self):
        self.lock = Lock()
        self.philosopher = 0
        self.queue = deque()

    def pickLeftFork(self):
        self.queue.append([self.philosopher, 1, 1])

    def pickRightFork(self):
        self.queue.append([self.philosopher, 2, 1])

    def putLeftFork(self):
        self.queue.append([self.philosopher, 1, 2])

    def putRightFork(self):
        self.queue.append([self.philosopher, 2, 2])

    def eat(self):
        # sleep(.2)
        self.queue.append([self.philosopher, 0, 3])

    # call the functions directly to execute, for example, eat()
    def wantsToEat(self,
                   philosopher: int,
                   pickLeftFork: 'Callable[[], None]',
                   pickRightFork: 'Callable[[], None]',
                   eat: 'Callable[[], None]',
                   putLeftFork: 'Callable[[], None]',
                   putRightFork: 'Callable[[], None]') -> None:
        self.lock.acquire()
        self.philosopher = philosopher
        pickLeftFork()
        pickRightFork()
        eat()
        putRightFork()
        putLeftFork()
        self.lock.release()
        sleep(.2)               # prove concurrency

    def run(self, philosopher: int, times: int):
        for i in range(times):
            self.wantsToEat(philosopher,
                            self.pickLeftFork,
                            self.pickRightFork,
                            self.eat,
                            self.putLeftFork,
                            self.putRightFork)


def main():
    dp = DiningPhilosophers()
    with futures.ThreadPoolExecutor(NUM) as executor:
        executor.map(dp.run, [i for i in range(NUM)], [2] * NUM)
    print([i for i in dp.queue])


if __name__ == "__main__":
    main()
