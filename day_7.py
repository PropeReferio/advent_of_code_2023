from argparse import ArgumentParser
from collections import Counter
from enum import StrEnum, auto
from operator import attrgetter
from pathlib import Path

from utils.files import list_input_lines


class HandTypeEnum(StrEnum):
    five_of_a_kind = auto()
    four_of_a_kind = auto()
    full_house = auto()
    three_of_a_kind = auto()
    two_pair = auto()
    one_pair = auto()
    high_card = auto()


class Hand:
    def __init__(self, hand: str, bid: int, part_two: bool):
        self.hand = hand
        self.bid = bid
        self.rank = None
        self.card_rankings = self.get_card_rankings(part_two=part_two)
        self.hand_type = self.get_hand_type(part_two=part_two)

    def get_hand_type(self, part_two=False):
        if part_two:
            cards_remaining = self.hand.replace("J", "")
            counter = Counter(cards_remaining)
            jokers = 5 - len(cards_remaining)
            counts = list(counter.values())
            counts.sort()
            if len(counts):
                counts[-1] += jokers
            else:
                counts = [5]
        else:
            counter = Counter(self.hand)
            counts = list(counter.values()).sort()
        if 5 in counts:
            return HandTypeEnum.five_of_a_kind
        elif 4 in counts:
            return HandTypeEnum.four_of_a_kind
        elif 3 in counts and 2 in counts:
            return HandTypeEnum.full_house
        elif 3 in counts:
            return HandTypeEnum.three_of_a_kind
        elif counts == [1, 2, 2]:
            return HandTypeEnum.two_pair
        elif 2 in counts:
            return HandTypeEnum.one_pair
        else:
            return HandTypeEnum.high_card

    def get_card_rankings(self, part_two):
        rankings = []
        card_values = {
            "A": 13,
            "K": 12,
            "Q": 11,
            "J": 0 if part_two else 10,
            "T": 9,
            "9": 8,
            "8": 7,
            "7": 6,
            "6": 5,
            "5": 4,
            "4": 3,
            "3": 2,
            "2": 1,
        }
        for card in self.hand:
            rankings.append(card_values[card])

        return rankings

    def __repr__(self):
        return f"Hand: {self.hand} Type: {self.hand_type} Cards Ranked: {self.card_rankings} Bid: {self.bid}"


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-p", "--part-one", action="store_true")
    args = parser.parse_args()
    testing: bool = args.testing
    part_one: bool = args.part_one

    lines = list_input_lines(Path(__file__), testing, True)

    hands_by_type = {
        HandTypeEnum.five_of_a_kind: [],
        HandTypeEnum.four_of_a_kind: [],
        HandTypeEnum.full_house: [],
        HandTypeEnum.three_of_a_kind: [],
        HandTypeEnum.two_pair: [],
        HandTypeEnum.one_pair: [],
        HandTypeEnum.high_card: [],
    }
    # Step 1: Make a list of hand objects
    hands = map_hands_to_bids(lines, part_two=not part_one)

    # Step 2: Make a new dict of rank: bid
    for hand in hands:
        hands_by_type[hand.hand_type].append(hand)

    # Step 3: sort hands_by_type by card_rankings property
    low_to_high = sort_hands_by_rank(hands_by_type)

    print_sum_winnings(low_to_high)


def sort_hands_by_rank(hands_by_type):
    for hand_type, hands_list in hands_by_type.items():
        hands_list.sort(key=attrgetter("card_rankings"), reverse=True)
    high_to_low = []
    for hand_type in [
        HandTypeEnum.five_of_a_kind,
        HandTypeEnum.four_of_a_kind,
        HandTypeEnum.full_house,
        HandTypeEnum.three_of_a_kind,
        HandTypeEnum.two_pair,
        HandTypeEnum.one_pair,
        HandTypeEnum.high_card,
    ]:
        high_to_low.extend(hands_by_type[hand_type])
    low_to_high = reversed(high_to_low)
    return low_to_high


def print_sum_winnings(low_to_high):
    # Step 3: Sum(rank * bid)
    winnings = []
    for i, hand in enumerate(low_to_high):
        winnings.append((i + 1) * hand.bid)
    print(winnings)
    print((sum(winnings)))


def map_hands_to_bids(lines, part_two: bool):
    hands = []
    for line in lines:
        split_line = line.split(" ")
        hand = Hand(split_line[0], int(split_line[1]), part_two)
        hands.append(hand)
    return hands


main()
