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


def generate_possible_paths(graph):
    paths = []
    # Call DFS on the graph. Always start at start, end at end,
    # Keep a visited graph where visited is always false for
    # big caves, and append paths to the list.
    paths = dfs(graph, paths, cur_path=[])

    return paths


def dfs(graph, paths, cur_path=[]):
    # I need to reset visited, somehow... or rather, just use
    # if small cave not in paths, go there and append.
    if len(cur_path) == 0:
        cur_path.append('start')

    cur_cave = cur_path[-1]
    if cur_cave == 'end':
        paths.append(cur_path)
        return paths
    # TODO cur_path doesn't get cleared... it goes back to the other
    # branch, but still has the cur_path of the original branch.


    for option in graph[cur_cave]:
        if option in cur_path and option.islower():
            continue
        else:
            cur_path.append(option)
            paths = dfs(graph, paths, cur_path)
            # TODO how do I reset the cur_path here?

    return paths


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
    possible_paths = generate_possible_paths(graph)
    print(f"Number of possible paths: {len(possible_paths)}")


main()
