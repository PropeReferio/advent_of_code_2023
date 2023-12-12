from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import List

from utils.files import list_input_lines


@dataclass
class Galaxy:
    y: int
    x: int

    def get_distance_to_other_galaxy(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


def expand_the_universe(
    universe: List[List[str]], part_one: bool = True
) -> List[List[str]]:
    with_columns_added: List[List[str]] = []
    columns_to_insert: List[int] = []
    replacement_character = "." if part_one else "*"
    for x in range(len(universe[0])):
        column = [row[x] for row in universe]
        if all([char == "." for char in column]):
            columns_to_insert.append(x)
    for row in universe:
        new_row = row
        expansions = 0
        for idx in columns_to_insert:
            new_row = (
                new_row[: idx + expansions]
                + replacement_character
                + new_row[idx + expansions :]
            )
            expansions += 1
        with_columns_added.append(new_row)
    with_rows_added: List[List[str]] = []
    for row in with_columns_added:
        with_rows_added.append(row)
        if all([char in {replacement_character, "."} for char in row]):
            with_rows_added.append(
                "".join([replacement_character for _ in range(len(row))])
            )

    return with_rows_added


def find_galaxies(expanded: List[List[str]], testing: bool = False) -> List[Galaxy]:
    part_two_distance = 99 if testing else 999_999
    list_of_galaxies: List[Galaxy] = []
    y = 0
    for row in expanded:
        x = 0
        if all([char == "*" for char in row]):
            y += part_two_distance
            continue
        else:
            y += 1
        for x_coord, char in enumerate(row):
            column = [row[x_coord] for row in expanded]
            if all([char == "*" for char in column]):
                x += part_two_distance
            else:
                x += 1
                if char == "#":
                    list_of_galaxies.append(Galaxy(y, x))

    return list_of_galaxies


def list_distances(list_of_galaxies: List[Galaxy]):
    distances: List[int] = []
    for idx, galaxy in enumerate(list_of_galaxies):
        for next_galaxy in list_of_galaxies[idx + 1 :]:
            distances.append(galaxy.get_distance_to_other_galaxy(next_galaxy))

    return distances


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-p", "--part-one", action="store_true")
    args = parser.parse_args()
    testing: bool = args.testing
    part_one: bool = args.part_one

    universe = list_input_lines(Path(__file__), testing, True)

    expanded = expand_the_universe(universe, part_one=part_one)
    pprint(expanded)
    list_of_galaxies: List[Galaxy] = find_galaxies(expanded, testing=testing)
    list_of_distances: List[int] = list_distances(list_of_galaxies)
    print(f"Length of distances list: {len(list_of_distances)}")

    print(sum(list_of_distances))


main()
