#! /usr/local/bin/python3

from collections import deque


def search(graph, name):
    q = deque()             # use FIFO te guarantee "breadth" first
    q += graph["you"]       # do not use append here
    done = []

    while q:
        e = q.popleft()
        if name == e:
            print("Found {}".format(e))
            return True
        if e not in done:
            done.append(e)
            q += graph[e]
    return False


def main():
    graph = {"you": ["alice", "bob", "claire"], "bob": ["anuj", "peggy"], "alice": ["peggy"],
             "claire": ["thom", "jonny"], "anuj": [], "peggy": [], "thom": [], "jonny": []}

    print(search(graph, "test"))
    print(search(graph, "thom"))


if __name__ == "__main__":
    main()
