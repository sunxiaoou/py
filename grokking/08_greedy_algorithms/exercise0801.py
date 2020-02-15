#! /usr/local/bin/python3


def greed(states_needed, stations):
    selected = []
    uncovered = states_needed

    while len(uncovered) > 0:
        print(uncovered)
        best_station = None
        covered = {}
        for station, states in stations.items():
            if station not in selected and len(covered) < len(states & states_needed):
                covered = states & states_needed
                best_station = station
        selected.append(best_station)
        uncovered -= covered

    print(selected)


def main():
    states_needed = {"mt", "wa", "or", "id", "nv", "ut", "ca", "az"}        # this is actually a set
    stations = {"kone": {"id", "nv", "ut"}, "ktwo": {"wa", "id", "mt"}, "kthree": {"or", "nv", "ca"},
                "kfour": {"nv", "ut"}, "kfive": {"ca", "az"}}

    greed(states_needed, stations)


if __name__ == "__main__":
    main()
