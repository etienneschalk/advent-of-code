from typing import Any, Sequence

from graphviz import Digraph


def construct_dot_graph_from_dict(graph_dict: dict[Any, Sequence[Any]]) -> Digraph:
    dot = Digraph()
    for node, children in graph_dict.items():
        fillcolor = "#ccffff"  # cyan = flipflop
        dot.node(f"{node}", style="filled", fillcolor=fillcolor)
        for child in children:
            dot.edge(f"{node}", f"{child}")
    return dot


def construct_dot_graph_from_couples(ordered_set: dict[Any, None]) -> Digraph:
    dot = Digraph()
    for key in ordered_set:
        source, target = key
        dot.edge(f"{source}", f"{target}", dir="both")

    return dot
