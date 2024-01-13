import numpy as np

from advent_of_code.common import (
    adapt_recursion_limit,
    load_input_text_file_from_filename,
)

ProblemDataType = dict[str, tuple[str, ...]]


def main():
    adapt_recursion_limit()
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    components = parse_input_text_file()
    # nodes_to_disconnect: thanks graphviz...
    nodes_to_disconnect = {"vgf": "jpn", "nmz": "mnl", "fdb": "txm"}
    #     Manual observation:
    # - vgf - jpn
    # - nmz - nml
    # - fdb - txm
    # nodes_to_explore = {"jpn", "nmz", "fdb"}
    nodes_to_explore = {"mpn", "nmz", "fdb"}
    disconnect_result = disconnect_then_explore(
        components, nodes_to_disconnect, nodes_to_explore
    )
    product_of_unique_group_sizes = compute_result_from_exploration(disconnect_result)
    unique_referenced_nodes = set.union(
        set(components.keys()), *[set(children) for children in components.values()]
    )
    # 1551
    # 601310
    assert len(unique_referenced_nodes) == sum(set(disconnect_result.values()))
    return product_of_unique_group_sizes


def compute_part_2():
    return None


def disconnect_then_explore(
    components: ProblemDataType,
    nodes_to_disconnect: dict[str],
    nodes_to_explore: set[str] | None = None,
) -> dict[str, int]:
    disconnected = {k: v for k, v in components.items()}
    for k, v in nodes_to_disconnect.items():
        disconnected[k] = tuple(child for child in disconnected[k] if child != v)

    if nodes_to_explore is None:
        nodes_to_explore = nodes_to_disconnect

    bidir = create_bidir(disconnected)
    bidir

    result = {}
    for start_node in nodes_to_explore:
        explored = set()
        explore_bidir(bidir, start_node, explored, 0)
        result[start_node] = len(explored)
    return result


def compute_result_from_exploration(result: dict[str, int]) -> int:
    return np.prod(list(set(result.values())))


def create_bidir(flat):
    flatset = {k: set(v) for k, v in flat.items()}
    futures = {}
    for node in flatset:
        for c in flatset[node]:
            if c in flatset:
                flatset[c].add(node)
            elif c in futures:
                futures[c].add(node)
            else:
                futures[c] = set()
    merged = {**flatset, **futures}
    return merged


def explore_bidir(
    flatset,
    start_node: str,
    explored: set[str],
    depth: int,
) -> None:
    explored.add(start_node)
    # print(depth)
    for child in flatset[start_node]:
        if child in explored:
            continue
        explore_bidir(flatset, child, explored, depth + 1)


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    # cmg: qnr nvd lhk bvb
    components = {}
    for line in lines:
        source, targets = line.split(": ")
        components[source] = tuple(targets.split(" "))
    return components


if __name__ == "__main__":
    main()
