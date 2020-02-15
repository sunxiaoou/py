#! /usr/local/bin/python3


def find_lowest_node(g):
    lowest_cost = float("inf")
    lowest_cost_node = None
    # Go through each node.
    for node in g.keys():
        cost = g[node][1]
        # If it's the lowest cost so far and hasn't been processed yet...
        if cost < lowest_cost and g[node][3] is False:
            # ... set it as the new lowest-cost node.
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node


def dijkstras(g):
    node = find_lowest_node(g)
    while node is not None:
        for neighbor in g[node][0].keys():
            if g[node][0][neighbor] + g[node][1] < g[neighbor][1]:
                g[neighbor][1] = g[node][0][neighbor] + g[node][1]      # update neighbor's lowest_cost
                g[neighbor][2] = node                                   # update neighbor's parent
            g[node][3] = True
        node = find_lowest_node(g)                                      # update node's processed flag
    return


def main():
    graph = {
        # node: [{neighbor1: weight1, ...}, lowest_cost, parent, processed]
        "start": [{"a": 6, "b": 2}, float("inf"), None, True],
        "a": [{"fin": 1}, 6, "start", False],
        "b": [{"a": 3, "fin": 5}, 2, "start", False],
        "fin": [{}, float("inf"), None, True]
    }

    graph = {
        "book": [{"rape_lp": 5, "poster": 0}, float("inf"), None, True],
        "rape_lp": [{"bass_guitar": 15, "drum_set": 20}, 5, "book", False],
        "poster": [{"bass_guitar": 30, "drum_set": 35}, 0, "book", False],
        "bass_guitar": [{"piano": 20}, float("inf"), None, False],
        "drum_set": [{"piano": 10}, float("inf"), None, False],
        "piano": [{}, float("inf"), None, True]
    }

    dijkstras(graph)

    print(graph)
    # node = "fin"
    node = "piano"
    while True:
        print("{}, {}".format(node, graph[node][1]))
        node = graph[node][2]
        if node is None:
            break


if __name__ == "__main__":
    main()
