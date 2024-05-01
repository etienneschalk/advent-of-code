from dataclasses import dataclass
from typing import Literal

import numpy as np
import plotly.graph_objects as go


@dataclass(frozen=True)
class ValuedLink:
    source: str
    target: str
    value: int


@dataclass(frozen=True)
class PlotlySankeyInput:
    labels: list[str]
    sources: list[int]
    targets: list[int]
    values: list[int]
    node_colors: list[str]
    link_colors: list[str]


def to_mapping_label_to_index(valued_links: list[ValuedLink]) -> dict[str, int]:
    collected_ordered_set: dict[str, None] = {}
    for link in valued_links:
        collected_ordered_set[link.source] = None
        collected_ordered_set[link.target] = None
    collected = {k: idx for idx, k in enumerate(collected_ordered_set)}
    return collected


def to_plotly_sankey_input(
    valued_links: list[ValuedLink],
    *,
    color_mode: Literal["random", "problem_202319"] = "random",
) -> PlotlySankeyInput:
    mapping_label_to_index = to_mapping_label_to_index(valued_links)

    sources = []
    targets = []
    values = []

    for link in valued_links:
        source_idx = mapping_label_to_index[link.source]
        target_idx = mapping_label_to_index[link.target]
        value = link.value
        sources.append(source_idx)
        targets.append(target_idx)
        values.append(value)

    labels = list(mapping_label_to_index)
    if color_mode == "random":
        random_color_array = np.random.randint(256, size=(len(sources), 3))
        node_colors = [f"rgb({r}, {g}, {b})" for (r, g, b) in random_color_array]
        link_colors = [f"rgba({r}, {g}, {b}, 0.3)" for (r, g, b) in random_color_array]
    elif color_mode == "problem_202319":
        mapping = {"A": "rgba(0,255,0,0.3)", "R": "rgba(255,0,0,0.3)"}
        node_colors = [mapping.get(node, "rgba(128,128,128,0.3)") for node in labels]
        mapping = {labels.index(k): v for k, v in mapping.items()}
        link_colors = [
            mapping.get(target, "rgba(128,128,128,0.3)") for target in targets
        ]

    else:
        raise NotImplementedError
    return PlotlySankeyInput(labels, sources, targets, values, node_colors, link_colors)


def build_sankey_figure(
    sankey_input: PlotlySankeyInput,
    title: str | None = None,
) -> go.Figure:
    node_style_dict = dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        color=sankey_input.node_colors,
    )
    fig = go.Figure(
        data=[
            go.Sankey(
                node={**dict(label=sankey_input.labels), **node_style_dict},
                link=dict(
                    source=sankey_input.sources,
                    target=sankey_input.targets,
                    value=sankey_input.values,
                    color=sankey_input.link_colors,
                ),
            )
        ]
    )

    title_text = title if title is not None else "Basic Sankey Diagram"
    fig.update_layout(title_text=title_text, font_size=10)
    return fig
