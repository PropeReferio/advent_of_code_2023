from argparse import ArgumentParser
from pprint import pprint


def get_initial_crabs(testing=False):
    if testing:
        with open("input/example_inputs/day_7.txt", "r") as read_file:
            crabs = read_file.read()
    else:
        with open("input/inputs/day_7.txt", "r") as read_file:
            crabs = read_file.read()

    crabs = list(map(lambda x: int(x), crabs.split(",")))

    return crabs


def calculate_fuel_at_position(
    target_position, cost_per_position_dict, crabs, cache, increasing=False
):
    fuel_consumed = 0
    for position in crabs:
        distance_to_travel = abs(target_position - position)
        if increasing:
            if distance_to_travel in cache.keys():
                fuel_consumed += cache[distance_to_travel]
            else:
                cache[distance_to_travel] = sum(
                    [1 + i for i in range(distance_to_travel)]
                )
                fuel_consumed += cache[distance_to_travel]
        else:
            fuel_consumed += distance_to_travel
    cost_per_position_dict[target_position] = fuel_consumed


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-i", "--increasing-cost", action="store_true")
    args = parser.parse_args()
    testing = args.testing
    increasing_cost = args.increasing_cost
    crabs = get_initial_crabs(testing)

    lowest_position = min(crabs)
    highest_position = max(crabs)
    range_to_check = range(lowest_position, highest_position + 1)
    cost_per_position_dict = {num: 0 for num in range_to_check}

    # Easy naive approach. Calculate the fuel required to move to each position, then
    # select the cheapest.
    cache = {}
    # Using a cache made the program way faster.
    for position in range_to_check:
        calculate_fuel_at_position(
            position, cost_per_position_dict, crabs, cache, increasing=increasing_cost
        )

    cheapest_alignment_position = get_cheapest_fuel_cost(cost_per_position_dict)

    print(cheapest_alignment_position)


def get_cheapest_fuel_cost(cost_per_position_dict):
    min_fuel_cost = None
    for value in cost_per_position_dict.values():
        if min_fuel_cost is None or (value < min_fuel_cost):
            min_fuel_cost = value
    return min_fuel_cost


main()
