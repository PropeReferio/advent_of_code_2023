import math
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple

from utils.files import list_input_lines


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-p", "--part-one", action="store_true")
    args = parser.parse_args()
    testing: bool = args.testing
    part_one: bool = args.part_one

    lines = list_input_lines(Path(__file__), testing, True)

    if part_one:
        times, times_distance_maps = parse_multiple_races_and_times(lines)
        ways_to_win = count_all_successes(times, times_distance_maps)

        print(math.prod(ways_to_win))
    else:
        record, time = parse_single_race_and_time(lines)

        count_failures_from_extreme_ends(record, time)


def count_all_successes(times, times_distance_maps):
    ways_to_win = []
    for time in times:
        victories = []
        for i in range(1, time):
            dist = i * (time - i)
            if dist > times_distance_maps[time]:
                victories.append(dist)
        ways_to_win.append(len(victories))
    return ways_to_win


def count_failures_from_extreme_ends(record, time):
    # Go both ways, from 0 forwards, and from 53897698 backwards. Count each attempt, each failure.
    # once you find a success, exit. subtract all your failures from the number time. that's your answer.
    failures = 0
    for i in range(1, time):
        if (time - i) * i > record:
            break
        else:
            failures += 1
    for j in range(time, 0, -1):
        if (time - j) * j > record:
            break
        else:
            failures += 1
    print(time - failures)


def parse_single_race_and_time(lines):
    time = lines[0].split(":")[1].strip().split(" ")
    time = int("".join(time))
    record = lines[1].split(":")[1].strip().split(" ")
    record = int("".join(record))
    return record, time


def parse_multiple_races_and_times(lines):
    times = lines[0].split(":")[1].strip().split(" ")
    times = [int(x) for x in times if x != ""]
    records = lines[1].split(":")[1].strip().split(" ")
    records = [int(x) for x in records if x != ""]
    times_distance_maps = dict(zip(times, records))
    return times, times_distance_maps


main()
