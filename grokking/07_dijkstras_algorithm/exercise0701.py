#! /usr/local/bin/python3

from pprint import pprint


INFINITY = float('inf')
NEIGHBORS = 0
LOWEST_COST = 1
PARENT = 2
PROCESSED = 3


def find_lowest_node(g):
    lowest_cost = INFINITY
    lowest_cost_node = None
    # Go through each node.
    for node in g.keys():
        cost = g[node][LOWEST_COST]
        # If it's the lowest cost so far and hasn't been processed yet...
        if cost < lowest_cost and g[node][PROCESSED] is False:
            # ... set it as the new lowest-cost node.
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node


def dijkstras(g):
    node = find_lowest_node(g)
    while node is not None:
        for neighbor in g[node][NEIGHBORS].keys():
            if g[node][NEIGHBORS][neighbor] + g[node][LOWEST_COST] < g[neighbor][LOWEST_COST]:
                # update neighbor's lowest_cost
                g[neighbor][LOWEST_COST] = g[node][NEIGHBORS][neighbor] + g[node][LOWEST_COST]
                # update neighbor's parent
                g[neighbor][PARENT] = node
            # update node's processed flag
            g[node][PROCESSED] = True
        node = find_lowest_node(g)
    return


def main():
    graph = {
        # node: [{neighbor1: weight1, ...}, lowest_cost, parent, processed]
        "start": [{"a": 6, "b": 2}, INFINITY, None, True],
        "a": [{"fin": 1}, 6, "start", False],
        "b": [{"a": 3, "fin": 5}, 2, "start", False],
        "fin": [{}, INFINITY, None, True]
    }

    graph = {
        "book": [{"rape_lp": 5, "poster": 0}, INFINITY, None, True],
        "rape_lp": [{"bass_guitar": 15, "drum_set": 20}, 5, "book", False],
        "poster": [{"bass_guitar": 30, "drum_set": 35}, 0, "book", False],
        "bass_guitar": [{"piano": 20}, INFINITY, None, False],
        "drum_set": [{"piano": 10}, INFINITY, None, False],
        "piano": [{}, INFINITY, None, True]
    }

    dijkstras(graph)

    pprint(graph)
    # node = "fin"
    node = "piano"
    while node is not None:
        print("{}, {}".format(node, graph[node][LOWEST_COST]))
        node = graph[node][PARENT]


if __name__ == "__main__":
    main()
