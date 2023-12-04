import math
from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
from typing import List, Dict, Set
from dataclasses import dataclass

from utils.files import list_input_lines


@dataclass
class PartNumWithCoords:
    num: int
    x_start: int
    x_end: int
    y: int

    def get_x_coord_range(self) -> range:
        return range(self.x_start - 1, self.x_end + 2)

    def get_tuple_representation(self) -> tuple:
        return self.num, self.x_start, self.x_end, self.y


@dataclass
class Star:
    x: int
    y: int
    numbers_adjacent: List[int]

    @property
    def line_before(self):
        return max(self.y - 1, 0)

    def line_after(self, num_of_rows):
        return min(self.y + 1, num_of_rows - 1)


def compare_two_lines_for_part_numbers(possible_part_nums: List[PartNumWithCoords], symbols: List[int], seen_nums: Set, part_numbers_total: int):
    if not len(symbols) or not len(possible_part_nums):
        return part_numbers_total
    for num_object in possible_part_nums:
        if num_object.get_tuple_representation() in seen_nums:
            continue
        for coord in symbols:
            if coord in num_object.get_x_coord_range():
                seen_nums.add(num_object.get_tuple_representation())
                part_numbers_total += num_object.num

    return part_numbers_total


def sum_all_gear_ratios(input_lines: List[str], gear_ratios: List[int]):

    def add_possible_part_num_and_clear_string(cur_num, possible_part_nums, x, y):
        if cur_num != '':
            possible_part_nums.append(
                PartNumWithCoords(int(cur_num), x - (len(cur_num)), x - 1, y)
            )
        return ''

    stars: List[Star] = []
    possible_gear_contacts: List[PartNumWithCoords] = []
    for y, line in enumerate(input_lines):
        cur_num = ''
        for x, char in enumerate(line+'.'):
            if char == '.':
                cur_num = add_possible_part_num_and_clear_string(cur_num, possible_gear_contacts, x, y)
            elif char.isdigit():
                cur_num += char
            elif char == '*':
                cur_num = add_possible_part_num_and_clear_string(cur_num, possible_gear_contacts, x, y)
                stars.append(Star(x, y, []))
            else:
                cur_num = add_possible_part_num_and_clear_string(cur_num, possible_gear_contacts, x, y)

    for star in stars:
        for num in possible_gear_contacts:
            if num.y in {star.line_before, star.line_after(len(input_lines)), star.y}:
                if star.x in num.get_x_coord_range():
                    star.numbers_adjacent.append(num.num)

        if len(star.numbers_adjacent) == 2:
            gear_ratios.append(math.prod(star.numbers_adjacent))


def sum_all_part_numbers(input_lines: List[str], part_numbers_total: int) -> Dict:

    def add_possible_part_num_and_clear_string(cur_num, possible_part_nums, x, y):
        if cur_num != '':
            possible_part_nums.append(
                PartNumWithCoords(int(cur_num), x - (len(cur_num)), x - 1, y)
            )
        return ''

    seen_nums = set()

    previous_possible_part_nums: List[PartNumWithCoords] = []
    previous_symbols: List[int] = []

    for y, line in enumerate(input_lines):
        possible_part_nums: List[PartNumWithCoords] = []
        symbols: List[int] = []
        cur_num = ''
        for x, char in enumerate(line + '.'):
            if char == '.':
                cur_num = add_possible_part_num_and_clear_string(cur_num, possible_part_nums, x, y)
            elif char.isdigit():
                cur_num += char
            else:
                cur_num = add_possible_part_num_and_clear_string(cur_num, possible_part_nums, x, y)
                symbols.append(x)

        # Compare current line with itself
        part_numbers_total = compare_two_lines_for_part_numbers(
            possible_part_nums,
            symbols,
            seen_nums,
            part_numbers_total
        )

        # Compare part nums from previous line with current line's symbols
        part_numbers_total = compare_two_lines_for_part_numbers(
            previous_possible_part_nums,
            symbols,
            seen_nums,
            part_numbers_total
        )

        # Compare part nums from current line with previous line's symbols
        part_numbers_total = compare_two_lines_for_part_numbers(
            possible_part_nums,
            previous_symbols,
            seen_nums,
            part_numbers_total
        )

        previous_possible_part_nums = deepcopy(possible_part_nums)
        previous_symbols = deepcopy(symbols)

    return part_numbers_total


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-p", "--part-one", action="store_true")
    args = parser.parse_args()
    testing: bool = args.testing
    part_one: bool = args.part_one

    lines = list_input_lines(Path(__file__), testing, part_one)
    # Treat this as a 2D matrix


    if part_one:
        part_numbers_total = 0
        part_numbers_total = sum_all_part_numbers(lines, part_numbers_total)

        print(part_numbers_total)
    else:
        gear_ratios: List[int] = []
        # When appending, add the product of the two numbers.

        sum_all_gear_ratios(lines, gear_ratios)

        print(sum(gear_ratios))


main()
