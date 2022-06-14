from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from pprint import pprint


def get_reactions_and_elements(testing=False):
    file_name = Path(__file__).parts[-1].replace(".py", ".txt")
    file_path = Path("./example_inputs" if testing else "./inputs").joinpath(file_name)
    with open(file_path, "r") as read_file:
        lines = read_file.read().split("\n")

    template = lines[0]
    reactions = {line.split(' -> ')[0]: line.split(' -> ')[1] for line in lines[2:]}

    return template, reactions


def insert_chemical_products(cur_elements, reactions):
    new_elements = list(cur_elements[0])
    # TODO improve time complexity
    for i in range(len(cur_elements) - 1):
        first, second = cur_elements[i], cur_elements[i+1]
        cur_pair = f"{first}{second}"
        new_elements.append(f"{reactions.get(cur_pair)}{second}")


    return ''.join(new_elements)


def get_most_and_least_common_elements(cur_elements):
    counter = Counter(cur_elements)
    most, least = counter.most_common()[0], counter.most_common()[-1]

    return most, least


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-l", "--long", action="store_true")
    args = parser.parse_args()
    testing = args.testing
    long = args.long
    template, reactions = get_reactions_and_elements(testing)

    cur_elements = template
    for _ in range(10 if not long else 20):
        cur_elements = insert_chemical_products(cur_elements, reactions)
    most, least = get_most_and_least_common_elements(cur_elements)

    print(f"Most minus least: {most[1] - least[1]}")


main()
