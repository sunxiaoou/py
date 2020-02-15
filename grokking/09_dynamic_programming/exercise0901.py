#! /usr/local/bin/python3


def knapsack(items, grid):
    for i in range(len(grid)):
        key = grid[i][0]
        time = items[key][0]
        rating = items[key][1]
        for j in range(1, len(grid[i])):
            if i == 0:
                if j < time:
                    grid[i][j] = ([], 0)
                else:
                    grid[i][j] = ([key], rating)
            else:
                last_cell = grid[i - 1][j]
                if j < time:
                    grid[i][j] = last_cell
                elif j == time:
                    if rating < last_cell[1]:
                        grid[i][j] = last_cell
                    else:
                        grid[i][j] = ([key], rating)
                else:
                    remaining_space = grid[i - 1][j - time]
                    if rating + remaining_space[1] < last_cell[1]:
                        grid[i][j] = last_cell
                    else:
                        grid[i][j] = ([key] + remaining_space[0], rating + remaining_space[1])
    return


def main():
    # "Attraction": (time, rating)
    items = {"WestminsterAbbey": (1, 7), "GlobeTheater": (1, 6), "NationalGallery": (2, 9), "BritishMuseum": (4, 9),
             "StPaulCathedral": (1, 8)
             }

    grid = [    # time       1     2     3     4
        ["WestminsterAbbey", None, None, None, None],
        ["GlobeTheater", None, None, None, None],
        ["NationalGallery", None, None, None, None],
        ["BritishMuseum", None, None, None, None],
        ["StPaulCathedral", None, None, None, None],
    ]

    knapsack(items, grid)

    """
    for r in grid:
        for c in r:
            if c is not None:
                print(c, end="\t")
        print()
    """

    print(grid[len(grid) - 1][len(grid[len(grid) - 1]) - 1])


if __name__ == "__main__":
    main()
