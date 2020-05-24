#! /usr/local/bin/python3
from typing import List


class Graph:
    def __init__(self, nv: int, edges: List[List[int]]):
        self.nv = nv
        self.ne = len(edges)
        self.adjacency = [[0] for _ in range(nv)]   # a[0] is in_degree
        for e in edges:
            self.adjacency[e[0]].append(e[1])
            self.adjacency[e[0]][0] += 1            # increase in_degree
        # assert not edges or max(max(e[0], e[1]) for e in edges) + 1 == nv


# this is a topological sort case
def findOrder(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    graph = Graph(numCourses, prerequisites)
    # print(graph.ne, graph.nv, graph.adjacency)
    res = []
    while True:
        for i in range(numCourses):
            if not graph.adjacency[i][0]:
                graph.adjacency[i][0] = -1
                res.append(i)
                break
        else:           # no V with in_degree 0, completed or happened cycle
            break
        for a in graph.adjacency:
            if i in a[1:]:      # decrease in_degree who depends on current V
                a[0] -= 1
    return res if len(res) == numCourses else []


def main():
    print(findOrder(3, [[1, 0], [1, 2], [0, 1]]))           # []
    print(findOrder(3, [[1, 0]]))                           # [0, 1, 2] or [2, 0, 1] or ...
    print(findOrder(1, []))                                 # [0]
    print(findOrder(2, [[1, 0]]))                           # [0, 1]
    print(findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))   # [0, 1, 2, 3] or [0, 2, 1, 3]
    edges = [[1, 0], [2, 0], [3, 0],
             [3, 1], [4, 1],
             [5, 2],
             [2, 3], [5, 3], [6, 3],
             [3, 4], [6, 4],
             [5, 6]]
    print(findOrder(7, edges))     # [0, 1, 4 , 3, 2, 6, 5]


if __name__ == "__main__":
    main()
