from argparse import ArgumentParser
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import List, Optional, Set, Tuple

from utils.files import list_input_lines


class CardinalDirection(StrEnum):
    N = auto()
    W = auto()
    E = auto()
    S = auto()

class PipeDirection(StrEnum):
    SEVEN = "7"
    L = "L"
    J = "J"
    F = "F"
    S = "S"
    NORTH_SOUTH = "|"
    EAST_WEST = "-"


@dataclass
class Pipe:
    direction: PipeDirection
    y: int
    x: int
    origin: Optional[CardinalDirection]

    @property
    def is_start(self) -> bool:
        return self.direction == PipeDirection.S

    @property
    def coords(self) -> Tuple[int, int]:
        return self.y, self.x

    def get_next_pipe(self, two_d_array: List[List[str]]):
        # Check above:
        if self.direction == PipeDirection.S:
            return self.get_next_pipe_after_start(two_d_array)
        if self.direction == PipeDirection.L:
            if self.origin == CardinalDirection.N:
                # Go east, origin W
                return Pipe(two_d_array[self.y][self.x + 1], self.y, self.x + 1, CardinalDirection.W)
            else:
                # Go north, origin S
                return Pipe(two_d_array[self.y - 1][self.x], self.y - 1, self.x, CardinalDirection.S)
        elif self.direction == PipeDirection.F:
            if self.origin == CardinalDirection.S:
                # Go east, origin W
                return Pipe(two_d_array[self.y][self.x + 1], self.y, self.x + 1, CardinalDirection.W)
            else:
                # Go south, origin N
                return Pipe(two_d_array[self.y + 1][self.x], self.y + 1, self.x, CardinalDirection.N)
        elif self.direction == PipeDirection.NORTH_SOUTH:
            if self.origin == CardinalDirection.N:
                # Go south, origin N
                return Pipe(two_d_array[self.y + 1][self.x], self.y + 1, self.x, CardinalDirection.N)
            else:
                # Go north, origin S
                return Pipe(two_d_array[self.y - 1][self.x], self.y - 1, self.x, CardinalDirection.S)
        elif self.direction == PipeDirection.SEVEN:
            if self.origin == CardinalDirection.S:
                # Go west, origin E
                return Pipe(two_d_array[self.y][self.x - 1], self.y, self.x - 1, CardinalDirection.E)
            else:
                # Go south, origin N
                return Pipe(two_d_array[self.y + 1][self.x], self.y + 1, self.x, CardinalDirection.N)
        elif self.direction == PipeDirection.EAST_WEST:
            if self.origin == CardinalDirection.W:
                # Go east, origin W
                return Pipe(two_d_array[self.y][self.x + 1], self.y, self.x + 1, CardinalDirection.W)
            else:
                # Go west, origin E
                return Pipe(two_d_array[self.y][self.x - 1], self.y, self.x - 1, CardinalDirection.E)
        elif self.direction == PipeDirection.J:
            if self.origin == CardinalDirection.N:
                # Go west, origin E
                return Pipe(two_d_array[self.y][self.x - 1], self.y, self.x - 1, CardinalDirection.E)
            else:
                # Go north, origin S
                return Pipe(two_d_array[self.y - 1][self.x], self.y - 1, self.x, CardinalDirection.S)

            # if self.y != 0:
            # node_above_value = two_d_array[self.y - 1][self.x]
            # node_above_coords = (self.y - 1, self.x)
            # if (
            #     node_above_value
            #     in {
            #         PipeDirection.SEVEN,
            #         PipeDirection.S,
            #         PipeDirection.F,
            #         PipeDirection.NORTH_SOUTH,
            #     }
            #     and node_above_coords not in seen
            # ):
                # Rather than checking all 4 directions, it is possible to go only in the valid directions...
                # For example, north and east for L. Pass in origin, only go the other way.
                # seen.add(node_above_coords)
                # return Pipe(node_above_value, self.y - 1, self.x)
        # if self.y != len(two_d_array) - 1:
        #     next_pipe_below = Pipe(two_d_array[self.y + 1][self.x], self.y + 1, self.x)
        #     if (
        #         next_pipe_below.direction
        #         in {
        #             PipeDirection.J,
        #             PipeDirection.S,
        #             PipeDirection.L,
        #             PipeDirection.NORTH_SOUTH,
        #         }
        #         and next_pipe_below.coords not in seen
        #     ):
                # TODO the above doesn't work. It does not constrain based on
                #  the direction of the current pipe.
                #  Try a property like valid_adjacent_pipes:
                #  if self.direction == PipeDirection.J:
                #      return {PipeDirection.S, PipeDirection.L, PipeDirection.F, PipeDirection.EAST_WEST}
                #  Consider composition: Turn the enum into a whole class, with the property above
                #  As a part of it.
                # seen.add((next_pipe_below.coords))
                # return next_pipe_below
        # if self.x != 0:
        #     next_pipe_right = Pipe(two_d_array[self.y][self.x - 1], self.y, self.x - 1)
        #     if (
        #         next_pipe_right.direction
        #         in {
        #             PipeDirection.F,
        #             PipeDirection.S,
        #             PipeDirection.L,
        #             PipeDirection.EAST_WEST,
        #         }
        #         and next_pipe_right.coords not in seen
        #     ):
        #         seen.add((next_pipe_right.coords))
        #         return next_pipe_right
        # if self.x != len(two_d_array[0]) - 1:
        #     next_pipe_right = Pipe(two_d_array[self.y][self.x + 1], self.y, self.x + 1)
        #     if (
        #         next_pipe_right.direction
        #         in {
        #             PipeDirection.SEVEN,
        #             PipeDirection.S,
        #             PipeDirection.J,
        #             PipeDirection.EAST_WEST,
        #         }
        #         and next_pipe_right.coords not in seen
        #     ):
        #         seen.add((next_pipe_right.coords))
        #         return next_pipe_right

    def get_next_pipe_after_start(self, two_d_array):
        # Find valid adjacent pipe
        northern_pipe = two_d_array[self.y - 1][self.x]
        southern_pipe = two_d_array[self.y + 1][self.x]
        eastern_pipe = two_d_array[self.y][self.x + 1]
        western_pipe = two_d_array[self.y][self.x - 1]
        if northern_pipe in {PipeDirection.F, PipeDirection.SEVEN,
                  PipeDirection.NORTH_SOUTH}:
            return Pipe(northern_pipe, self.y - 1, self.x, CardinalDirection.S)
        elif southern_pipe in {PipeDirection.NORTH_SOUTH, PipeDirection.J,
                            PipeDirection.L}:
            return Pipe(southern_pipe, self.y + 1, self.x, CardinalDirection.N)
        elif eastern_pipe in {PipeDirection.EAST_WEST, PipeDirection.J,
                    PipeDirection.SEVEN}:
            return Pipe(southern_pipe, self.y, self.x + 1, CardinalDirection.W)
        else:
            return Pipe(western_pipe, self.y, self.x - 1, CardinalDirection.E)


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-p", "--part-one", action="store_true")
    args = parser.parse_args()
    testing: bool = args.testing
    part_one: bool = args.part_one

    two_d_array = list_input_lines(Path(__file__), testing, True)

    start = get_start(two_d_array)

    # Start by assuming that the input will not pipe us out of the edge of the array
    cur_node = start
    steps = 0
    # seen = set()
    # seen.add(start.coords)

    while True:
        cur_node: Pipe = cur_node.get_next_pipe(two_d_array)
        steps += 1
        if cur_node.direction == "S":
            break

    halfway_distance = steps / 2
    print(halfway_distance)
    # cur_node = start
    # steps = 0
    #
    # while steps != halfway_distance:
    #     cur_node: Pipe = cur_node.get_next_pipe(two_d_array)
    #     steps += 1


    # if part_one:
    #     print(sum([hist.extrapolated_value for hist in value_histories]))
    # else:
    #     print(sum([hist.reverse_extrapolated_value for hist in value_histories]))


def get_start(two_d_array: List[List[str]]) -> Pipe:
    for i, row in enumerate(two_d_array):
        for j, value in enumerate(two_d_array[i]):
            if value == PipeDirection.S:
                start = Pipe(PipeDirection.S, i, j, None)
    return start


main()
