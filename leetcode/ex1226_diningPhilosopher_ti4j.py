#! /usr/local/bin/python3
from concurrent import futures
from threading import Lock
from time import sleep
from typing import List
NUM = 5


class Fork:
    def __init__(self):
        self.picked = False
        self.lock = Lock()

    def pick(self):
        self.lock.acquire()
        self.picked = True

    def put(self):
        self.picked = False
        self.lock.release()


class Philosopher:
    def __init__(self, num: int, fork1: Fork, fork2: Fork):
        self.id = num
        self.left = fork1
        self.right = fork2

    def pickLeftFork(self) -> List:
        self.left.pick()
        return [self.id, 1, 1]

    def pickRightFork(self) -> List:
        self.right.pick()
        return [self.id, 2, 1]

    def putLeftFork(self) -> List:
        self.left.put()
        return [self.id, 1, 2]

    def putRightFork(self) -> List:
        self.right.put()
        return [self.id, 2, 2]

    def eat(self) -> List:
        sleep(.2)
        return [self.id, 0, 3]


def wantsToEat(philosopher: Philosopher):
    print(philosopher.pickLeftFork())
    print(philosopher.pickRightFork())
    print(philosopher.eat())
    print(philosopher.putRightFork())
    print(philosopher.putLeftFork())


def main():
    forks = [Fork() for i in range(NUM)]
    philosophers = [Philosopher(i, forks[i], forks[(i + 1) % NUM]) for i in range(NUM)]
    with futures.ThreadPoolExecutor(NUM) as executor:
        result = executor.map(wantsToEat, philosophers)
    print(list(result))


if __name__ == "__main__":
    main()
