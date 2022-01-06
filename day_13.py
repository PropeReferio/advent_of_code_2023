from argparse import ArgumentParser
from pathlib import Path
from pprint import pprint


def get_paper_dots(testing=False):
    file_name = Path(__file__).parts[-1].replace(".py", ".txt")
    file_path = Path("./example_inputs" if testing else "./inputs").joinpath(file_name)
    with open(file_path, "r") as read_file:
        lines = read_file.read().split("\n")

    coords = []
    fold_instructions = []

    for line in lines:
        if ',' in line:
            x, y = line.split(',')
            coords.append((int(x), int(y)))
        elif 'f' in line:
            fold_instructions.append(line)

    dots_paper = get_dots(coords)
    fold_instructions = get_fold_instructions(fold_instructions)

    return dots_paper, fold_instructions


def get_dots(coords):
    x_axis_len = max([coord[0] for coord in coords])
    y_axis_len = max([coord[1] for coord in coords])
    grid = [['.' for _ in range(x_axis_len + 1)] for _ in range(y_axis_len + 1)]
    for coord in coords:
        x, y = coord
        grid[y][x] = '#'

    return grid


def get_fold_instructions(fold_instructions):
    final = []
    for instruction in fold_instructions:
        direction, value = instruction.split("=")
        direction = direction[-1]
        final.append((direction, int(value)))

    return final


def fold(dots_paper, instruction):
    direction = instruction[0]
    fold_line = instruction[1]
    if direction == 'y':
        for y in range(fold_line+1, len(dots_paper)):
            cur_line = dots_paper[y]
            for x, symbol in enumerate(cur_line):
                if symbol == '#':
                    dist_from_fold = y - fold_line
                    dots_paper[fold_line - dist_from_fold][x] = '#'
        dots_paper = dots_paper[0:fold_line]

    elif direction == 'x':
        for x in range(fold_line+1, len(dots_paper[0])):
            cur_col = []
            for line in dots_paper:
                cur_col.append(line[x])
            for y, symbol in enumerate(cur_col):
                if symbol == '#':
                    dist_from_fold = x - fold_line
                    dots_paper[y][fold_line - dist_from_fold] = '#'
        # Lose remainder of paper:
        dots_paper = [line[0:fold_line] for line in dots_paper]

    return dots_paper


def count_hashes(dots_paper):
    num_hashes = 0
    for y in range(len(dots_paper)):
        for x in range(len(dots_paper[0])):
            if dots_paper[y][x] == '#':
                num_hashes += 1

    return num_hashes


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-s", "--single", action="store_true")
    args = parser.parse_args()
    testing = args.testing
    single = args.single
    dots_paper, fold_instructions = get_paper_dots(testing)

    for instruction in fold_instructions:
        dots_paper = fold(dots_paper, instruction)
        if single:
            break

    if single:
        num_hashes = count_hashes(dots_paper)
        print(num_hashes)
    else:
        for line in dots_paper:
            print(line)


main()
