from argparse import ArgumentParser
from pprint import pprint


def get_characters(testing=False):
    file_path = "./example_inputs/day_10.txt" if testing else "./inputs/day_10.txt"
    with open(file_path, "r") as read_file:
        rows = read_file.read().split("\n")

    return rows


def determine_remaining_chars(stack):
    remaining_chars = []
    opposite_brace = {"[": "]", "(": ")", "{": "}", "<": ">"}
    for char in stack[::-1]:
        remaining_chars.append(opposite_brace[char])

    return remaining_chars


def score_remaining_chars(remaining_chars):
    completion_scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    score = 0
    for char in remaining_chars:
        score *= 5
        score += completion_scores[char]

    return score


def score_row_of_chars(row, complete=False):

    bracket_pairs = {"}": "{", "]": "[", ")": "(", ">": "<"}

    bracket_scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    stack = []
    broken = False
    for char in row:
        if len(stack) == 0:
            stack.append(char)
        else:
            if char in bracket_pairs:
                last_char = stack.pop()
                if last_char == bracket_pairs[char]:
                    continue
                else:
                    if not complete:
                        return bracket_scores[char]
                    else:
                        broken = True
                        break
            else:
                stack.append(char)
    if not complete:
        return 0
    else:
        if broken:
            return
        else:
            remaining_chars = determine_remaining_chars(stack)
            return score_remaining_chars(remaining_chars)


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-c", "--complete", action="store_true")
    args = parser.parse_args()
    testing = args.testing
    complete = args.complete
    rows = get_characters(testing)
    if complete:
        scores = []
        for row in rows:
            scores.append(score_row_of_chars(row, complete))
        scores = list(filter(lambda el: el is not None, scores))
        scores.sort()
        middle_index = len(scores) // 2
        return scores[middle_index]
    else:
        score = 0
        for row in rows:
            row_score = score_row_of_chars(row)
            score += row_score

        return score


print(main())
