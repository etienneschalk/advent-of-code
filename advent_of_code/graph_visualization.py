from typing import Any, Literal, Mapping, Sequence

from graphviz import Digraph  # pyright: ignore[reportMissingTypeStubs]


# Note: Use Mapping instead of dict because Mapping is covariant (so it can accept specializations)
def construct_dot_graph_from_dict(
    graph_dict: Mapping[Any, Sequence[Any]],
    *,
    dir: Literal["forward", "back", "both", "none"] = "forward",
    nodesep: float = 0.25,
) -> Digraph:
    dot = Digraph()
    dot.attr(nodesep=str(nodesep))
    for node, children in graph_dict.items():
        fillcolor = "#ccffff"  # cyan = flipflop
        dot.node(f"{node}", style="filled", fillcolor=fillcolor)
        for child in children:
            dot.edge(f"{node}", f"{child}", dir=dir, labeltooltip=f"{node} to {child}")
    return dot


def construct_dot_graph_from_couples(ordered_set: Mapping[Any, None]) -> Digraph:
    dot = Digraph()
    for key in ordered_set:
        source, target = key
        dot.edge(f"{source}", f"{target}", dir="both")

    return dot
