#! /ux/local/bin/python3
from typing import List


def turnpike(distances: List[int], n_stat: int) -> List[int]:
    print(distances)
    stations = [-1] * n_stat
    stations[0] = 0                     # first station
    stations[-1] = max(distances)       # last station
    distances.remove(stations[-1])

    def place(left: int, right: int) -> bool:
        if not distances:
            return True

        x = max(distances)              # try to set stations[right]
        relates = [x - s for s in stations[:left]] + [s - x for s in stations[right + 1:]]
        r2 = []
        for d in relates:
            if d not in distances:
                distances.extend(r2)
                break
            distances.remove(d)
            r2.append(d)
        else:                                   # current level is OK
            stations[right] = x
            found = place(left, right - 1)      # recurse subsequents
            if found:                           # all subsequents are OK
                return True
            else:
                print('backtracking ...')
                stations[right] = -1            # backtracking current level
                distances.extend(relates)

        x = stations[-1] - max(distances)       # try to set station[left]
        relates = [x - s for s in stations[:left]] + [s - x for s in stations[right + 1:]]
        r2 = []
        for d in relates:
            if d not in distances:
                distances.extend(r2)
                break
            distances.remove(d)
            r2.append(d)
        else:
            stations[left] = x
            found = place(left + 1, right)
            if found:
                return True
            else:
                print('backtracking ...')
                stations[left] = -1
                distances.extend(relates)
        return False

    place(1, n_stat - 2)
    return stations


def main():
    print(turnpike([1, 2, 2, 2, 3, 3, 3, 4, 5, 5, 5, 6, 7, 8, 10], 6))  # d = n * (n - 1) / 2


if __name__ == "__main__":
    main()
