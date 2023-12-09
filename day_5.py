from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple

from utils.files import list_input_lines


@dataclass
class SourceDestValues:
    dest: int
    source: int
    _range: int

    @property
    def dest_source_difference(self) -> int:
        return self.source - self.dest

    @property
    def range_object(self) -> range:
        return range(self.source, self.source + self._range)


def parse_source_dest_values(line):
    parts = line.split(" ")
    return SourceDestValues(int(parts[0]), int(parts[1]), int(parts[2]))


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-p", "--part-one", action="store_true")
    args = parser.parse_args()
    testing: bool = args.testing
    part_one: bool = args.part_one

    lines = list_input_lines(Path(__file__), testing, True)

    seed_to_soil_map = list()
    soil_to_fertilizer_map = list()
    fertilizer_to_water_map = list()
    water_to_light_map = list()
    light_to_temperature_map = list()
    temperature_to_humidity_map = list()
    humidity_to_location_map = list()

    ordered_dicts = [
        seed_to_soil_map,
        soil_to_fertilizer_map,
        fertilizer_to_water_map,
        water_to_light_map,
        light_to_temperature_map,
        temperature_to_humidity_map,
        humidity_to_location_map,
    ]

    seeds: List[int] = list(
        map(lambda x: int(x), lines[0].split(":")[1].strip().split(" "))
    )
    if not part_one:
        seeds = parse_seed_ranges(seeds)
    parse_almanac_mappings(lines, ordered_dicts)
    locations: List[int] = get_location_values_for_seeds(ordered_dicts, seeds)
    print(min(locations))


def get_location_values_for_seeds(ordered_dicts, seeds):
    locations: List[int] = []
    for seed in seeds:
        cur_val = seed
        for mapping in ordered_dicts:
            for value_object in mapping:
                if cur_val in value_object.range_object:
                    cur_val = cur_val - value_object.dest_source_difference
                    break

        locations.append(cur_val)


def parse_almanac_mappings(lines, ordered_dicts):
    cur_dict_idx = 0
    for line in lines[3:]:
        if line == "":
            cur_dict_idx += 1
        elif line[0].isdigit():
            source_dest_values: SourceDestValues = parse_source_dest_values(line)
            ordered_dicts[cur_dict_idx].append(source_dest_values)


def parse_seed_ranges(seeds):
    seeds_start_values = seeds[0::2]
    seeds_range_values = seeds[1::2]
    seeds = []
    for i, start_val in enumerate(seeds_start_values):
        seeds.extend(list(range(start_val, start_val + seeds_range_values[i])))
    print(len(seeds))
    return seeds


main()
