#! /usr/local/bin/python3


def regression(history, today, number):
    distances = []
    for day in history:
        # Pythagorean formula
        distance = \
            (day[0] - today[0]) * (day[0] - today[0]) + \
            (day[1] - today[1]) * (day[1] - today[1]) + \
            (day[2] - today[2]) * (day[2] - today[2])
        distances.append((distance, day[3]))

    distances.sort(key=lambda x: x[0])
    print(distances)

    s = 0
    n = number if number <= len(history) else len(history)
    for i in range(n):
        s += distances[i][1]

    return s / n


def main():
    history = [(5, 1, 0, 300), (3, 1, 1, 225), (1, 1, 0, 75), (4, 0, 1, 200), (4, 0, 0, 150), (2, 0, 0, 50)]
    today = (4, 1, 0)

    print(regression(history, today, 4))


if __name__ == "__main__":
    main()
