from argparse import ArgumentParser
from pprint import pprint


def get_grid(testing=False):
    if testing:
        with open("input/example_inputs/day_9.txt", "r") as read_file:
            rows = read_file.read().split("\n")
    else:
        with open("input/inputs/day_9.txt", "r") as read_file:
            rows = read_file.read().split("\n")

    grid = [[int(height) for height in row] for row in rows]
    return grid


def is_low_point(cell, grid, i, j):
    row_length = len(grid[0]) - 1
    column_length = len(grid) - 1
    if i < column_length:
        if cell >= grid[i + 1][j]:
            return False
    if i > 0:
        if cell >= grid[i - 1][j]:
            return False
    if j < row_length:
        if cell >= grid[i][j + 1]:
            return False
    if j > 0:
        if cell >= grid[i][j - 1]:
            return False

    return True


def dfs(grid, visited, y, x, basin_size, basin_sizes):
    if (
        y < 0
        or x < 0
        or y >= len(grid)
        or x >= len(grid[0])
        or visited[y][x]
        or grid[y][x] == 9
    ):
        return
    basin_size += 1
    visited[y][x] = True
    dfs(grid, visited, y + 1, x, basin_size, basin_sizes)
    dfs(grid, visited, y - 1, x, basin_size, basin_sizes)
    dfs(grid, visited, y, x + 1, basin_size, basin_sizes)
    dfs(grid, visited, y, x - 1, basin_size, basin_sizes)
    basin_sizes.append(basin_size)


def get_basin_sizes(grid, visited, basin_sizes, real_basin_sizes):
    for y, row in enumerate(grid):
        for x, height in enumerate(row):
            basin_size = 0
            basin_sizes = []
            if grid[y][x] != 9 and visited[y][x] is False:
                dfs(grid, visited, y, x, basin_size, basin_sizes)
                real_basin_sizes.append(len(basin_sizes))


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-b", "--basins", action="store_true")
    args = parser.parse_args()
    testing = args.testing
    basins = args.basins
    grid = get_grid(testing)
    if basins:
        visited = [[False for height in row] for row in grid]
        basin_sizes = []
        real_basin_sizes = []
        get_basin_sizes(grid, visited, basin_sizes, real_basin_sizes)
        real_basin_sizes.sort()
        print(real_basin_sizes[-1] * real_basin_sizes[-2] * real_basin_sizes[-3])
    else:
        low_points = []
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if is_low_point(cell, grid, i, j):
                    low_points.append(cell)

        print(sum(low_points) + len(low_points))


main()
