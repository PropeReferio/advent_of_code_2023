from argparse import ArgumentParser
from pathlib import Path
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass

from utils.files import list_input_lines


@dataclass
class ScratchCard:
    winning_nums: Set[int]
    nums_you_have: Set[int]

    @property
    def total_winning_nums(self) -> int:
        return len(self.nums_you_have.intersection(self.winning_nums))

    def get_card_score(self) -> int:
        if self.total_winning_nums == 0:
            return 0
        else:
            return 2 ** (self.total_winning_nums - 1)


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-p", "--part-one", action="store_true")
    args = parser.parse_args()
    testing: bool = args.testing
    part_one: bool = args.part_one

    lines = list_input_lines(Path(__file__), testing, True)
    scratchcards = parse_scratchcards(lines)

    if part_one:
        score_sum = 0
        for card in scratchcards:
            score_sum += card.get_card_score()

        print(score_sum)

    else:
        quantity_of_each_card_mapping = {idx: 1 for idx in range(len(scratchcards))}
        num_cards_processed = 0
        for idx, card in enumerate(scratchcards):
            for _ in range(quantity_of_each_card_mapping[idx]):
                num_cards_processed += 1
                for j in range(1, card.total_winning_nums + 1):
                    quantity_of_each_card_mapping[idx + j] += 1

        print(num_cards_processed)


def parse_scratchcards(lines):
    scratchcards: List[ScratchCard] = []
    for line in lines:
        _, remainder = line.split(':')
        winning_side, own_side = remainder.split('|')
        winning_nums: List[int] = []
        own_nums: List[int] = []
        for string in winning_side.split(' '):
            if string.isdigit():
                winning_nums.append(int(string))
        for string in own_side.split(' '):
            if string.isdigit():
                own_nums.append(int(string))

        scratchcards.append(ScratchCard(set(winning_nums), set(own_nums)))

    return scratchcards


main()
