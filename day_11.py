from argparse import ArgumentParser
from pprint import pprint


def get_octopi(testing=False):
    file_name = __file__.split("/")[-1].replace("py", "txt")
    file_path = f"./example_inputs/{file_name}" if testing else f"./inputs/{file_name}"
    with open(file_path, "r") as read_file:
        rows = read_file.read().split("\n")
        grid = [[int(num) for num in row] for row in rows]

    return grid


def increment_all_energy_by_one(grid):
    grid = [[num + 1 for num in row] for row in grid]
    return grid


def flash_single_octopus_and_increment_adjacent(grid, x, y, total_flashes):
    if grid[y][x] == 0:
        # If an octopus is at 0, it has already flashed. Therefore don't
        # increment anything.
        return
    total_flashes += 1
    grid[y][x] = 0
    # Increment all adjacent octopi.
    boundary = range(10)
    for y_adj in range(-1, 2):
        for x_adj in range(-1, 2):
            if (
                x_adj == 0
                and y_adj == 0
                or not y + y_adj in boundary
                or not x + x_adj in boundary
            ):
                continue
            else:
                if grid[y + y_adj][x + x_adj] != 0:
                    grid[y + y_adj][x + x_adj] += 1
    return grid, total_flashes


def flash_octopi(grid, total_flashes):
    for y, row in enumerate(grid):
        for x, octopus in enumerate(row):
            if octopus > 9:
                grid, total_flashes = flash_single_octopus_and_increment_adjacent(
                    grid, x, y, total_flashes
                )

    return grid, total_flashes


def grid_still_needs_flashing(grid):
    for y, row in enumerate(grid):
        for x, octopus in enumerate(row):
            if octopus > 9:
                return True
    return False


def take_a_step(grid, total_flashes):
    grid = increment_all_energy_by_one(grid)
    while grid_still_needs_flashing(grid):
        grid, total_flashes = flash_octopi(grid, total_flashes)
    return grid, total_flashes


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-s", "--simultaneous", action="store_true")
    args = parser.parse_args()
    testing = args.testing
    simultaneous = args.simultaneous
    grid = get_octopi(testing)
    total_flashes = 0
    step = 0
    if not simultaneous:
        for _ in range(100):
            grid, total_flashes = take_a_step(grid, total_flashes)
    else:
        while True:
            grid, total_flashes = take_a_step(grid, total_flashes)
            step += 1
            if simultaneous:
                if sum([sum([octopus for octopus in row]) for row in grid]) == 0:
                    return step

    # How many total flashes are there after 100 steps?
    return total_flashes


print(main())
