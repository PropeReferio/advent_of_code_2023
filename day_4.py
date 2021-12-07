def create_boards():
    with open("./inputs/day_4.txt", "r") as rf:
        boards = rf.read().split("\n\n")
    call_numbers = boards[0].split(",")
    boards = boards[1:]
    boards_array = [board.split("\n") for board in boards]
    boards_array = [[strng.split(" ") for strng in board] for board in boards_array]
    new_boards_array = []
    for board in boards_array:
        new_board = []
        for line in board:
            new_line = list(filter(lambda x: len(x) > 0, line))
            new_board.append(new_line)
        new_boards_array.append(new_board)
    for board in new_boards_array:
        if len(board) != 5:
            raise Exception("improper board")
        for line in board:
            if len(line) != 5:
                raise Exception("improper board")
    marked = [
        [[False, False, False, False, False] for line in board]
        for board in new_boards_array
    ]

    return new_boards_array, marked, call_numbers


def mark_num_on_boards(num, new_boards_array, marked):
    for i, board in enumerate(new_boards_array):
        for j, line in enumerate(board):
            for k, el in enumerate(line):
                if num == el:
                    marked[i][j][k] = True


def calculate_sum_unmarked(winning_board, winning_marked):
    """
    Get the sum of all unmarked numbers.
    :param new_boards_array:
    :param marked:
    :return: (int) score
    """
    sum = 0
    for i, row in enumerate(winning_marked):
        for j, el in enumerate(row):
            if el is False:
                sum += int(winning_board[i][j])
    return sum


def check_board_for_win(board, marked, wins):
    """
    :param marked:
    :param board:
    :return: (tuple) boolean for victory, score (0 if no victory)
    """
    victory, unmarked_sum = False, 0
    for i, row in enumerate(marked):
        for j, el in enumerate(board):
            column = [marked[l][j] for l in range(5)]
            if all(row) or all(column):
                # 5 in a row
                victory = True
                unmarked_sum = calculate_sum_unmarked(board, marked)
                break
    return victory, unmarked_sum


def main():
    new_boards_array, marked, call_numbers = create_boards()
    wins = 0
    winning_boards = set()
    for num in call_numbers:
        mark_num_on_boards(num, new_boards_array, marked)
        for i, board in enumerate(new_boards_array):
            if i in winning_boards:
                continue
            victory, unmarked_sum = check_board_for_win(board, marked[i], wins)
            if victory:
                print(f"Board #{i} won with score: {unmarked_sum * int(num)}")
                winning_boards.add(i)


main()
