from argparse import ArgumentParser
from pathlib import Path
from pprint import pprint


def get_cave_edges(testing=False):
    file_name = Path(__file__).parts[-1].replace(".py", ".txt")
    file_path = Path("./example_inputs" if testing else "./inputs").joinpath(file_name)
    with open(file_path, "r") as read_file:
        edges = read_file.read().split("\n")

    return edges


def generate_graph(edges):
    graph = {}
    for edge in edges:
        left, right = edge.split('-')
        if left not in graph:
            graph[left] = []
        graph[left].append(right)
        if right not in graph:
            graph[right] = []
        graph[right].append(left)

    return graph


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--testing", action="store_true")
    parser.add_argument("-s", "--simultaneous", action="store_true")
    args = parser.parse_args()
    testing = args.testing
    simultaneous = args.simultaneous
    edges = get_cave_edges(testing)
    graph = generate_graph(edges)
    pprint(graph)


main()
