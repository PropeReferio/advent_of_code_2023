from argparse import ArgumentParser
from pathlib import Path
from typing import List, Optional

from utils.files import list_input_lines


class ValuesHistory:
    def __init__(self, history):
        self.history: List[int] = history
        self.lists_of_differences: List[int] = self.get_lists_of_differences()

    def get_lists_of_differences(self):
        cur_diff: Optional[List[int]] = None
        diffs: List[List[int]] = []
        while True:
            if not cur_diff:
                cur_diff = []
                for i, num in enumerate(self.history[1:], start=1):
                    cur_diff.append(num - self.history[i - 1])
                diffs.append(cur_diff)
            else:
                new_diff = []
                for i, num in enumerate(cur_diff[1:], start=1):
                    new_diff.append(num - cur_diff[i - 1])
                diffs.append(new_diff)
                cur_diff = new_diff
                if all([val == 0 for val in cur_diff]):
                    break
        return diffs

    @property
    def extrapolated_value(self):
        return self.history[-1] + sum(
            [_list[-1] for _list in self.lists_of_differences]
        )

    @property
    def reverse_extrapolated_value(self):
        cur_num = 0
        reversed = self.lists_of_differences[::-1] + [self.history]
        for i, diff in enumerate(reversed, start=1):
            cur_num = diff[0] - cur_num

        return cur_num


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-p", "--part-one", action="store_true")
    args = parser.parse_args()
    testing: bool = args.testing
    part_one: bool = args.part_one

    lines = list_input_lines(Path(__file__), testing, True)
    value_histories = [
        ValuesHistory(list(map(lambda val: int(val), line.split(" "))))
        for line in lines
    ]

    if part_one:
        print(sum([hist.extrapolated_value for hist in value_histories]))
    else:
        print(sum([hist.reverse_extrapolated_value for hist in value_histories]))


main()
