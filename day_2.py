import math
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Dict

from utils.files import list_input_lines

CUBES_MAP = {"red": 12, "green": 13, "blue": 14}
COLORS = {"red", "green", "blue"}


def turn_round_into_dict(round: List[str]) -> Dict[str, int]:
    color_dict = dict()
    for color in round:
        num = int(''.join([char for char in color if char.isdigit()]))
        for _color_item in COLORS:
            if _color_item in color:
                color_dict[_color_item] = num

    return color_dict


def parse_cube_game_lines(input_lines: List[str]) -> Dict:
    games_map: dict = {}
    for line in input_lines:
        id_str, data_string = line.split(':')
        game_id = int(''.join([char for char in id_str if char.isdigit()]))
        games_map[game_id] = []
        rounds = [round.split(',') for round in data_string.split(';')]
        for round in rounds:
            round_dict = turn_round_into_dict(round)
            games_map[game_id].append(
                round_dict
            )

    return games_map


def is_game_possible(game_data: List[Dict]) -> bool:
    for round in game_data:
        for color, num in round.items():
            if CUBES_MAP[color] < num:
                return False

    return True


def get_least_possible_cubes_per_game(game_data: List[Dict]) -> List[int]:
    least_possible_cubes = {'red': 0, 'blue': 0, 'green': 0}
    for _round in game_data:
        for color in COLORS:
            least_possible_cubes[color] = max(least_possible_cubes[color], _round.get(color, 0))

    return list(least_possible_cubes.values())



def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-p", "--part-one", action="store_true")
    args = parser.parse_args()
    testing: bool = args.testing
    part_one: bool = args.part_one

    lines = list_input_lines(Path(__file__), testing, part_one)

    games_dict = parse_cube_game_lines(lines)

    if part_one:
        ids_total = 0
        for game_id, game_data in games_dict.items():
            if is_game_possible(game_data):
                ids_total += game_id

        print(ids_total)
    else:
        powers_sum = 0
        for game_data in games_dict.values():
            least_possible_cubes_per_game: List[int] = get_least_possible_cubes_per_game(game_data)
            powers_sum += math.prod(least_possible_cubes_per_game)

        print(powers_sum)


main()
