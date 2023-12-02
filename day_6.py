from argparse import ArgumentParser
from collections import Counter

# How many lanternfish would there be after 80 days?


def get_initial_fish(testing=False):
    if testing:
        with open("input/example_inputs/day_6.txt", "r") as read_file:
            fish = read_file.read()
    else:
        with open("input/inputs/day_6.txt", "r") as read_file:
            fish = read_file.read()

    fish = list(map(lambda x: int(x), fish.split(",")))

    return fish


def pass_a_day_fish_cycle(fish_day_dict):
    # Step 1: If there are 14 0-day fish, eliminate those
    # and create 14 6-day and 14 8-day fish.
    sixes = eights = fish_day_dict[0]
    # Step 2: Move all 3-day fish to 2-day, 2-day fish to 1-day, etc.
    zeroes = fish_day_dict[1]
    ones = fish_day_dict[2]
    twoes = fish_day_dict[3]
    threes = fish_day_dict[4]
    fours = fish_day_dict[5]
    fives = fish_day_dict[6]
    sixes += fish_day_dict[7]
    sevens = fish_day_dict[8]

    dict_after_day_passes = {
        0: zeroes,
        1: ones,
        2: twoes,
        3: threes,
        4: fours,
        5: fives,
        6: sixes,
        7: sevens,
        8: eights,
    }

    return dict_after_day_passes


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-d", "--days", type=int)
    args = parser.parse_args()
    testing = args.testing
    days = args.days
    fish = get_initial_fish(testing)

    fish_day_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0} | dict(
        Counter(fish)
    )

    for _ in range(days):
        fish_day_dict = pass_a_day_fish_cycle(fish_day_dict)

    print(sum(fish_day_dict.values()))


main()
