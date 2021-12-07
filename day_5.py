from argparse import ArgumentParser
from pprint import pprint


def convert_text_to_coordinates(testing=False):
    """
    Takes the text input and returns data useable by
    Python
    :return:
    """
    if testing:
        with open("./example_inputs/day_5.txt", "r") as read_file:
            line_points = read_file.read().split("\n")
    else:
        with open("./inputs/day_5.txt", "r") as read_file:
            line_points = read_file.read().split("\n")

    line_points = [coord.split(" -> ") for coord in line_points]
    return line_points


def add_vert_horiz_line_to_grid(start, stop, grid):
    """
    Increments points on the grid where the line falls.
    """
    if start[0] == stop[0]:
        seg_begin, seg_end = sorted([int(start[1]), int(stop[1])])
        for y_coord in range(seg_begin, seg_end + 1):
            grid[y_coord][int(start[0])] += 1
    elif start[1] == stop[1]:
        seg_begin, seg_end = sorted([int(start[0]), int(stop[0])])
        for x_coord in range(seg_begin, seg_end + 1):
            grid[int(start[1])][x_coord] += 1


def add_diagonal_line_to_grid(start, stop, grid):
    x_diff_positive = int(stop[0]) > int(start[0])
    y_diff_positive = int(stop[1]) > int(start[1])
    length = abs(int(stop[1]) - int(start[1]))
    cur_point = (int(start[0]), int(start[1]))
    grid[cur_point[1]][cur_point[0]] += 1
    for i in range(length):
        new_x_coord = cur_point[0] + 1 if x_diff_positive else cur_point[0] - 1
        new_y_coord = cur_point[1] + 1 if y_diff_positive else cur_point[1] - 1
        cur_point = (new_x_coord, new_y_coord)
        grid[cur_point[1]][cur_point[0]] += 1


def is_line_vert_or_horiz(start, stop):
    """
    Returns True if horizontal or vertical.
    :return: boolean
    """
    return start[0] == stop[0] or start[1] == stop[1]


def calculate_danger_points(grid):
    count = 0
    for lst in grid:
        for element in lst:
            if element > 1:
                count += 1
    return count


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument(
        "-d", "--diagonal", action="store_true", help="Count diagonal lines also."
    )
    args = parser.parse_args()
    testing = args.testing
    diagonal = args.diagonal
    line_points = convert_text_to_coordinates(testing=testing)

    # Step 2: Create 999 x 999 grid that increments values when a line crosses a point
    grid = [
        [0 for i in range(10 if testing else 1000)]
        for _ in range(10 if testing else 1000)
    ]

    # Step 3: Add horizontal and vertical lines to grid
    for line_seg in line_points:
        start, stop = line_seg[0].split(","), line_seg[1].split(",")
        if diagonal:
            if is_line_vert_or_horiz(start, stop):
                add_vert_horiz_line_to_grid(start, stop, grid)
            else:
                add_diagonal_line_to_grid(start, stop, grid)
        else:
            if not is_line_vert_or_horiz(start, stop):
                continue
            add_vert_horiz_line_to_grid(start, stop, grid)

    # Step 4: Score the grid: Find points with a value of 2 or higher
    danger_points = calculate_danger_points(grid)
    print(danger_points)
    if testing:
        pprint(grid)


main()
