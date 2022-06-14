from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from pprint import pprint


def get_reactions_and_elements(testing=False):
    file_name = Path(__file__).parts[-1].replace(".py", ".txt")
    file_path = Path("./example_inputs" if testing else "./inputs").joinpath(file_name)
    with open(file_path, "r") as read_file:
        pass


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-l", "--long", action="store_true")
    args = parser.parse_args()
    testing = args.testing
    long = args.long


main()
