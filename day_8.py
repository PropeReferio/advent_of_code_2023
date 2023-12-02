from argparse import ArgumentParser


def get_display_output(testing=False):
    if testing:
        with open("input/example_inputs/day_8.txt", "r") as read_file:
            display = read_file.read().split("\n")
    else:
        with open("input/inputs/day_8.txt", "r") as read_file:
            display = read_file.read().split("\n")

    return display


def decode_sample(sample) -> dict:
    """
    Takes the gibberish sample and figures out which digit is which.
    :param sample:
    :return: A dict with nums as keys, and strings like 'be' as values.
    """
    final = {str(num): "" for num in range(10)}
    for word in sample.split(" "):
        if len(word) == 2:
            final["1"] = word
        elif len(word) == 3:
            final["7"] = word
        elif len(word) == 4:
            final["4"] = word
        elif len(word) == 7:
            final["8"] = word
    # 1, 4, and 7 all share the right side of the display.
    # Ex: 1: 'be', 4: 'cgeb', 7: 'edb'... 'eb' is the right side.
    both_right_segments = final["1"]
    # What the 8 has that the other unique digits don't is the bottom
    # and bottom left.
    bottom_left_and_bottom_set = (
        set(final["8"]) - set(final["7"]) - set(final["4"]) - set(final["1"])
    )
    bottom_left_and_bottom = "".join([letter for letter in bottom_left_and_bottom_set])
    # 3 is the only 5 segment digit that uses the whole right side...
    # so from there, you can find the 3.
    for word in sample.split(" "):
        if len(word) == 5:
            if set(both_right_segments) < set(word):
                # Means set('be') is a subset of set('fegab')
                final["3"] = word
            elif set(bottom_left_and_bottom) < set(word):
                final["2"] = word
            else:
                final["5"] = word
        elif len(word) == 6:
            if set(both_right_segments) < set(word):
                # if both_right_segments in word:
                if set(bottom_left_and_bottom) < set(word):
                    final["0"] = word
                else:
                    final["9"] = word
            else:
                final["6"] = word

    return final


def calculate_value_on_display(dict_decoded, display_value):
    flipped_dict = {v: k for k, v in dict_decoded.items()}
    final = ""
    for digit in display_value.split(" "):
        for key, value in flipped_dict.items():
            if len(key) == len(digit) and len(set(digit) & set(key)) == len(key):
                final += value
                break
    return int(final)


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-d", "--decode", action="store_true")
    args = parser.parse_args()
    testing = args.testing
    decode = args.decode
    display = get_display_output(testing)
    # sample_digits = list(map(lambda x: x.split("|")[0], display))
    # values = list(map(lambda x: x.split("|")[1], display))
    sample_digits, values = [], []
    for screen in display:
        sample, value = screen.split("|")
        sample_digits.append(sample.strip())
        values.append(value.strip())
    if not decode:
        easy_digits = 0
        for screen in values:
            for digit in screen.split(" "):
                if len(digit) in [2, 3, 4, 7]:
                    easy_digits += 1
        return f"Easy digits: {easy_digits}"
    else:
        running_total_of_values = 0
        for i, sample in enumerate(sample_digits):
            dict_decoded = decode_sample(sample)
            running_total_of_values += calculate_value_on_display(
                dict_decoded, values[i]
            )
        return running_total_of_values


print(main())
