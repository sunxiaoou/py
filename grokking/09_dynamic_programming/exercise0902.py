#! /usr/local/bin/python3


def create_grid(typo, guess):
    grid = []
    line0 = ["\\"] + [char for char in typo]
    grid.append(line0)
    for char in guess:
        line = [char] + [0] * len(typo)
        grid.append(line)
    return grid


def print_grid(grid):
    for r in grid:
        for c in r:
            print(c, end="\t")
        print()
    print()


def longest_common_subsequence(typo, guess):
    grid = create_grid(typo, guess)
    # print_grid(grid)
    result = []
    for i in range(1, len(grid)):
        for j in range(1, len(grid[i])):
            if grid[i][0] != grid[0][j]:
                up_cell = 0 if i == 1 else grid[i - 1][j]
                left_cell = 0 if j == 1 else grid[i][j - 1]
                grid[i][j] = max(up_cell, left_cell)
            else:
                up_left_cell = 0 if i == 1 or j == 1 else grid[i - 1][j - 1]
                grid[i][j] = up_left_cell + 1
                result = [i, j, grid[i][j]]
    print_grid(grid)
    return result


def main():
    print(longest_common_subsequence("hish", "fish"))
    print(longest_common_subsequence("hish", "vista"))
    # print(longest_common_subsequence("fosh", "fort"))
    # print(longest_common_subsequence("fosh", "fish"))


if __name__ == "__main__":
    main()
