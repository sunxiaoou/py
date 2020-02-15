#! /usr/local/bin/python3

from collections import deque


def search(name):
    graph = {"you": ["alice", "bob", "claire"], "bob": ["anuj", "peggy"], "alice": ["peggy"],
             "claire": ["thom", "jonny"], "anuj": [], "peggy": [], "thom": [], "jonny": []}

    q = deque()
    q += graph["you"]       # not append here
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
    print(search("test"))
    print(search("thom"))


if __name__ == "__main__":
    main()
