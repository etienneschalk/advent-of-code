from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202325 import (
    compute_result_from_exploration,
    disconnect_then_explore,
    parse_text_input,
)


def test_problem_202325_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    components = parse_text_input(test_input)
    assert components == {
        "jqt": ("rhn", "xhk", "nvd"),
        "rsh": ("frs", "pzl", "lsr"),
        "xhk": ("hfx",),
        "cmg": ("qnr", "nvd", "lhk", "bvb"),
        "rhn": ("xhk", "bvb", "hfx"),
        "bvb": ("xhk", "hfx"),
        "pzl": ("lsr", "hfx", "nvd"),
        "qnr": ("nvd",),
        "ntq": ("jqt", "hfx", "bvb", "xhk"),
        "nvd": ("lhk",),
        "lsr": ("lhk",),
        "rzs": ("qnr", "cmg", "lsr", "rsh"),
        "frs": ("qnr", "lhk", "lsr"),
    }

    nodes_to_disconnect = {"cmg": "bvb", "jqt": "nvd", "pzl": "hfx"}
    # nodes_to_disconnect: thanks graphviz...
    nodes_to_explore = set(nodes_to_disconnect.keys())
    disconnect_result = disconnect_then_explore(
        components, nodes_to_disconnect, nodes_to_explore
    )
    assert disconnect_result == {"pzl": 9, "jqt": 6, "cmg": 9}
    product_of_unique_group_sizes = compute_result_from_exploration(disconnect_result)
    unique_referenced_nodes = set.union(
        set(components.keys()), *[set(children) for children in components.values()]
    )
    assert len(unique_referenced_nodes) == sum(set(disconnect_result.values()))
    assert product_of_unique_group_sizes == 6 * 9
