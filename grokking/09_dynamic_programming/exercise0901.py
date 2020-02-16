#! /usr/local/bin/python3


KEYS = 0
RATTING = 1


def knapsack(items, grid):
    for i in range(1, len(grid)):
        key = grid[i][0]
        cost = items[key][0]
        rating = items[key][1]
        for j in range(1, len(grid[i])):
            space = grid[0][j]
            if i == 1:
                if space < cost:
                    grid[i][j] = ([], 0)
                else:
                    grid[i][j] = ([key], rating)
            else:
                last_cell = grid[i - 1][j]
                if space < cost:
                    grid[i][j] = last_cell
                elif space == cost:
                    if rating < last_cell[RATTING]:
                        grid[i][j] = last_cell
                    else:
                        grid[i][j] = ([key], rating)
                else:
                    remaining_space_cell = grid[i - 1][space - cost]
                    if rating + remaining_space_cell[RATTING] < last_cell[RATTING]:
                        grid[i][j] = last_cell
                    else:
                        grid[i][j] = ([key] + remaining_space_cell[KEYS], rating + remaining_space_cell[RATTING])
    return


def main():
    # "Attraction": (time cost, rating)
    items = {"WestminsterAbbey": (1, 7), "GlobeTheater": (1, 6), "NationalGallery": (2, 9), "BritishMuseum": (4, 9),
             "StPaulCathedral": (1, 8)
             }

    grid = [    # time       1     2     3     4
        ["\\", 1, 2, 3, 4],
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
