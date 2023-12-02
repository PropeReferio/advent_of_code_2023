from pathlib import Path


def list_input_lines(file, testing=False, part_one=True):
    file_name = file.parts[-1].replace(".py", ".txt")
    if part_one:
        file_path = Path("./input/example_inputs" if testing else "./input/inputs").joinpath(file_name)
    else:
        file_path = Path("./input/examples_part_two" if testing else "./input/inputs_part_two").joinpath(file_name)
    with open(file_path, "r") as read_file:
        lines = read_file.read().split("\n")

    return lines
