from typing import Any, Callable

import numpy as np
import pandas as pd
import xarray as xr
from pyobsplot import Plot

from advent_of_code.y_2023.problem_202311 import get_compartiments


def visualize_puzzle_input_202311(
    space_xda: xr.DataArray,
    *,
    with_rules: bool = False,
    with_graph: bool = False,
    coord_array: xr.DataArray | None = None,
    edge_density: float | None = None,
    with_chunk_graph: bool = False,
    **kwargs: Any,
):
    def callback(marks: list[Any]) -> None:
        if with_graph:
            if coord_array is None:
                raise ValueError(
                    "coord_array was not given, it is needed to visualize the graph"
                )

            if edge_density is None:
                _edge_density = 1
            else:
                _edge_density = edge_density

            _coord_array = coord_array + 0.5

            lines = []
            for idx, pair_source in enumerate(_coord_array.values.tolist()):
                for pair_target in _coord_array.values[idx + 1 :].tolist():
                    lines.append([pair_source, pair_target])

            # Only display a subset of all the links
            period = int(1 / _edge_density)
            lines = lines[::period]

            table = {
                "x1": [],
                "y1": [],
                "x2": [],
                "y2": [],
            }

            for line in lines:
                table["y1"].append(line[0][0])
                table["x1"].append(line[0][1])
                table["y2"].append(line[1][0])
                table["x2"].append(line[1][1])

            table = pd.DataFrame.from_dict(table)
            marks.append(
                Plot.link(
                    table,
                    {
                        "x1": "x1",
                        "y1": "y1",
                        "x2": "x2",
                        "y2": "y2",
                        "stroke": "white",
                        "strokeWidth": 0.3,
                    },
                )
            )

        if with_rules:
            row_chunks = get_compartiments(space_xda, "row", "col")
            col_chunks = get_compartiments(space_xda, "col", "row")

            marks.append(
                Plot.ruleY(
                    [chunk.start - 0.5 for chunk in list(row_chunks.values())[1:]],
                    {"stroke": "red"},
                ),
            )
            marks.append(
                Plot.ruleX(
                    [chunk.start - 0.5 for chunk in list(col_chunks.values())[1:]],
                    {"stroke": "red"},
                ),
            )

        if with_chunk_graph:
            row_chunks = get_compartiments(space_xda, "row", "col")
            col_chunks = get_compartiments(space_xda, "col", "row")

            points = []
            row_middles = [np.mean(v) for v in row_chunks.values()]
            col_middles = [np.mean(v) for v in col_chunks.values()]
            for row_middle in row_middles:
                for col_middle in col_middles:
                    points.append([col_middle, row_middle])

            marks.append(
                Plot.dot(
                    points,
                    {"stroke": "#00ff00"},
                ),
            )

            with_chunk_rules = True
            if with_chunk_rules:
                marks.append(
                    Plot.ruleY(
                        row_middles,
                        {"stroke": "#00ff00", "strokeWidth": 0.5},
                    ),
                )
                marks.append(
                    Plot.ruleX(
                        col_middles,
                        {"stroke": "#00ff00", "strokeWidth": 0.5},
                    ),
                )

    return build_base_xarray_plot(space_xda, callback, **kwargs)


def build_base_xarray_plot(
    xda: xr.DataArray,
    callback: Callable[[list[Any]], None],
    *,
    dark_mode: bool = True,
    scale: float = 1,
):
    # Callback is a consumer of list of marks that enrich it.
    grid = (xda == ord("#")).astype(int) * 255
    marks = []
    marks.append(
        Plot.axisX({"anchor": "top"}),
    )
    marks.append(
        Plot.raster(
            grid.values.reshape(-1),
            {
                "width": grid.col.size,
                "height": grid.row.size,
                "imageRendering": "pixelated",
            },
        ),
    )

    callback(marks)

    if dark_mode:
        style = {
            "backgroundColor": "#111111",
            "color": "#eeeeee",
        }
    else:
        style = {}

    return Plot.plot(
        {
            # weight seems to break aspectRatio
            # whereas width does not, hence it is kept.
            # "height": 140 * 4 * scale,
            "width": 140 * 4 * scale,
            "color": {"scheme": "magma"},
            "x": {"domain": [0, grid.col.size], "label": "column"},
            "y": {"domain": [grid.row.size, 0], "label": "row"},
            "marks": marks,
            "style": style,
            "aspectRatio": 1,
        }
    )
