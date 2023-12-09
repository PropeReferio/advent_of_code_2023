from argparse import ArgumentParser
from pathlib import Path
from typing import List

WORD_NUMBERS_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_calibration_input(testing=False) -> List[str]:
    file_name = Path(__file__).parts[-1].replace(".py", ".txt")
    file_path = Path("./example_inputs" if testing else "./inputs").joinpath(file_name)
    with open(file_path, "r") as read_file:
        lines = read_file.read().split("\n")

    return lines


def get_nums_from_input(all_nums: List[int], input: str, words: bool = False):
    first_digit, last_digit = None, None
    cur_string = ""
    for char in input:
        cur_string += char
        if char.isdigit():
            if first_digit is None:
                first_digit = char
            last_digit = char
        elif words:
            for k, v in WORD_NUMBERS_MAP.items():
                if cur_string.endswith(k):
                    if first_digit is None:
                        first_digit = v
                    last_digit = v
    all_nums.append(
        int(first_digit + last_digit if last_digit else first_digit + first_digit)
    )


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-w", "--words", action="store_true")
    args = parser.parse_args()
    testing = args.testing
    words_also = args.words
    inputs = get_calibration_input(testing)

    all_nums: List[int] = []

    if words_also:
        for input in inputs:
            get_nums_from_input(all_nums, input, words=words_also)
    else:
        for input in inputs:
            get_nums_from_input(all_nums, input)

    print(sum(all_nums))


main()
