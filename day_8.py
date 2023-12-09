import math
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple

from utils.files import list_input_lines


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-p", "--part-one", action="store_true")
    args = parser.parse_args()
    testing: bool = args.testing
    part_one: bool = args.part_one

    lines = list_input_lines(Path(__file__), testing, part_one)

    graph_nodes, which_ways, starting_nodes = parse_directions(lines, part_one=part_one)

    steps = 0

    if part_one:
        cur_node = starting_nodes[0]
        while cur_node != "ZZZ":
            idx = steps % len(which_ways)
            if which_ways[idx] == "L":
                cur_node = graph_nodes[cur_node][0]
            else:
                cur_node = graph_nodes[cur_node][1]
            steps += 1
        pass
    else:
        print(which_ways)
        print(graph_nodes)
        print(steps)
        cur_nodes = starting_nodes
        while not all([node.endswith("Z") for node in cur_nodes]):
            idx = steps % len(which_ways)
            for i, node in enumerate(cur_nodes):
                if which_ways[idx] == "L":
                    cur_nodes[i] = graph_nodes[node][0]
                else:
                    cur_nodes[i] = graph_nodes[node][1]
            steps += 1


def parse_directions(lines, part_one=True):
    which_ways = [char for char in lines[0]]
    graph_nodes = {}
    if part_one:
        starting_nodes = ["AAA"]
    else:
        starting_nodes = []
    for line in lines[2:]:
        start, fork = line.split("=")
        start = start.strip()
        if start.endswith("A"):
            starting_nodes.append(start)
        left, right = fork.replace("(", "").replace(")", "").replace(" ", "").split(",")
        graph_nodes[start.strip()] = (left, right)
    return graph_nodes, which_ways, starting_nodes


main()
