from dataclasses import dataclass, field, replace
from typing import Any, Callable, Literal, Self

import numpy as np
import pandas as pd
import xarray as xr
from pyobsplot import Obsplot, Plot

from advent_of_code.y_2023.problem_202311 import get_compartiments


def create_obsplot_instance(
    *,
    renderer: Literal["jsdom", "widget"] = "jsdom",
    theme: Literal["current", "light", "dark"] = "dark",
):
    # See https://juba.github.io/pyobsplot/usage.html#renderers

    return Obsplot(renderer=renderer, theme=theme)


# This is a singleton instance of observable plot, allowing further customization like
# changing the renderer from 'widget' to 'json'.

op_instance = create_obsplot_instance(renderer="jsdom", theme="dark")


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
                Plot.link(  # type:ignore
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
                Plot.ruleY(  # type:ignore
                    [chunk.start - 0.5 for chunk in list(row_chunks.values())[1:]],
                    {"stroke": "red"},
                ),
            )
            marks.append(
                Plot.ruleX(  # type:ignore
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
                Plot.dot(  # type:ignore# type:ignore
                    points,
                    {"stroke": "#00ff00"},
                ),
            )

            with_chunk_rules = True
            if with_chunk_rules:
                marks.append(
                    Plot.ruleY(  # type:ignore
                        row_middles,
                        {"stroke": "#00ff00", "strokeWidth": 0.5},
                    ),
                )
                marks.append(
                    Plot.ruleX(  # type:ignore
                        col_middles,
                        {"stroke": "#00ff00", "strokeWidth": 0.5},
                    ),
                )

    return build_base_xarray_plot(space_xda, callback, **kwargs)


def visualize_puzzle_input_202310(
    xda: xr.DataArray,
    *,
    text_xda: xr.DataArray | None = None,
    **kwargs: Any,
):
    def callback(marks: list[Any]) -> None:
        if text_xda is not None:
            df = text_xda.stack(z=("row", "col")).to_pandas()
            data = df.values.tolist()
            rows = [idx[0] + 0.5 for idx in df.index]
            cols = [idx[1] + 0.5 for idx in df.index]
            marks.append(
                Plot.text(  # type:ignore
                    data,
                    {
                        "text": Plot.identity,  # type: ignore
                        "x": cols,
                        "y": rows,
                        "color": "white",
                        "fontSize": 38 * kwargs["width"] / 600 * 13 / xda["col"].size,
                    },
                )
            )

    return build_base_xarray_plot(
        xda, callback, margin=0, do_convert_ascii_array_to_uint8=False, **kwargs
    )


def visualize_puzzle_input_202324(
    lines_df: pd.DataFrame,
    *,
    rock_df: pd.DataFrame | None = None,
    width: int = 800,
    strokeWidth: float = 2,
    strokeOpacity: float = 1,
    x_domain_test_area: tuple[float, float] = (7, 27),
    y_domain_test_area: tuple[float, float] = (7, 27),
    do_highlight_text: bool = False,
    scheme: str = "Observable10",
    rock_text_fill: str = "#faa",
    rock_strokeWidth: float = 2,
    rock_strokeDasharray: str = "3",
    reverse_yx_axes: bool = True,
    title: str | None = None,
) -> Obsplot:
    """Visualize the Puzzle Input of 202324.

    This function draws 2D vectors that are stored in a ``DataFrame``

    Parameters
    ----------
    lines_df
        DataFrame with columns [x1 y1 x2 y2 time_in_ns]
        representing a hailstone relative position vector
    rock_df
        DataFrame with columns [x1 y1 x2 y2 time_in_ns]
        representing a rock relative position vector
    width
        Width of the produced plot
    strokeWidth
        Stroke width of hailstones' relative position vectors
    strokeOpacity
        Stroke opacity of hailstones' relative position vectors
    x_domain_test_area
        x-domain of the test area, materialized by a box in the plot
    y_domain_test_area
        x-domain of the test area, materialized by a box in the plot
    do_highlight_text
        De-clutter text mark by removing some of them. Useful for busy plots with many vectors
    scheme
        Categorical color scheme used to draw vectors. The colors depends of its time
    rock_text_fill
        Text Fill for the Text Mark used to annotate the time above the rock's trajectory
    rock_strokeWidth
        Stroke width of the rock's relative position vectors
    rock_strokeDasharray
        Stroke Dash Array pattern of the rock's relative position vectors
    reverse_yx_axes
        Flip the axis (useful to convert a portrait-plot to a landscape one, saving space)
    title
        Title of the plot

    Returns
    -------
        An Observable Plot
    """
    if reverse_yx_axes:
        x1_target = "y1"
        x2_target = "y2"
        y1_target = "x1"
        y2_target = "x2"
        x_target = "y"
        y_target = "x"
    else:
        x1_target = "x1"
        x2_target = "x2"
        y1_target = "y1"
        y2_target = "y2"
        x_target = "x"
        y_target = "y"

    marks = [
        Plot.link(  # type:ignore
            lines_df,
            {
                x1_target: lines_df["x1"].to_list(),
                y1_target: lines_df["y1"].to_list(),
                x2_target: lines_df["x2"].to_list(),
                y2_target: lines_df["y2"].to_list(),
                "markerEnd": "arrow",
                "curve": "linear",
                "strokeWidth": strokeWidth,
                "strokeOpacity": strokeOpacity,
                "stroke": lines_df["time_in_ns"].to_list(),
            },
        ),
        Plot.rect(  # type:ignore
            pd.DataFrame.from_records(
                {
                    x1_target: [x_domain_test_area[0]],
                    x2_target: [x_domain_test_area[1]],
                    y1_target: [y_domain_test_area[0]],
                    y2_target: [y_domain_test_area[1]],
                }
            ),
            {
                x1_target: "x1",
                y1_target: "y1",
                x2_target: "x2",
                y2_target: "y2",
                "stroke": "currentColor",
            },
        ),
        Plot.text(  # type:ignore
            lines_df,
            {
                x_target: lines_df["x2"].to_list(),
                y_target: lines_df["y2"].to_list(),
                "text": lines_df["time_in_ns"].to_list(),
                "fill": "currentColor",
                "stroke": "black",
                "dy": -12,
                # Only keep some text to avoid clutter
                "filter": "highlight" if do_highlight_text else None,
            },
        ),
    ]

    if rock_df is not None:
        marks.extend(
            [
                Plot.link(  # type:ignore
                    rock_df,
                    {
                        x1_target: rock_df["x1"].to_list(),
                        y1_target: rock_df["y1"].to_list(),
                        x2_target: rock_df["x2"].to_list(),
                        y2_target: rock_df["y2"].to_list(),
                        "markerEnd": "arrow",
                        "strokeOpacity": 1,
                        "curve": "linear",
                        "strokeWidth": rock_strokeWidth,
                        "strokeDasharray": rock_strokeDasharray,
                        # stroke=rock_df["time_in_ns"].to_list(),
                        "stroke": "red",
                        # headAngle=30,
                    },
                ),
                Plot.text(  # type:ignore
                    rock_df,
                    {
                        x_target: rock_df["x2"].to_list(),
                        y_target: rock_df["y2"].to_list(),
                        "text": rock_df["time_in_ns"].to_list(),
                        "fill": rock_text_fill,
                        "stroke": "black",
                        "dy": -12,
                    },
                ),
            ]
        )

    return op_instance(  # type: ignore
        dict(
            grid=True,
            x=dict(
                label=x_target,
                tickFormat=".0s",
                nice=True,
                # domain=list(x_domain),
                ticks=10,
            ),
            y=dict(
                label=y_target,
                tickFormat=".0s",
                nice=True,
                # domain=list(y_domain),
                ticks=10,
            ),
            color={"type": "categorical", "scheme": scheme},
            marks=marks,
            aspectRatio=1,
            width=width,
            title=title,
        )
    )


MarkProducerSignature = Callable[[], list[Any]]


@dataclass(kw_only=True, frozen=True)
class ObservablePlotXarrayBuilder:
    _marks_producers: list[MarkProducerSignature] = field(default_factory=list)
    _op: Obsplot = op_instance
    raster_xda: xr.DataArray
    initial_kwargs: dict[str, Any]

    def copy(self, *, raster_xda: xr.DataArray, **kwargs: Any) -> Self:
        # For convenience, allow to alter the initial_kwargs when copying.
        # Any passed kwarg will override any existing one on the original builder.
        updated_kwargs = {**self.initial_kwargs, **kwargs}
        return replace(
            self,
            raster_xda=raster_xda,
            initial_kwargs=updated_kwargs,
        )

    def build_marks(self) -> list[Any]:
        marks = []
        for marks_producer in self._marks_producers:
            produced_marks = marks_producer()
            marks.extend(produced_marks)
        return marks

    def append(self, mark_producer: MarkProducerSignature) -> Self:
        self._marks_producers.append(mark_producer)
        return self

    def plot(
        self,
        dark_mode: bool = True,
        scale: float = 1,
        width: int = 140 * 4,
        do_convert_ascii_array_to_uint8: bool = True,
        **kwargs: Any,
    ) -> Obsplot:
        raster_xda = self.raster_xda

        if do_convert_ascii_array_to_uint8 and raster_xda.dtype == np.uint8:
            raster_xda = (raster_xda == ord("#")).astype(int)  # * 255

        raster_width = raster_xda["col"].size
        raster_height = raster_xda["row"].size

        marks = []
        marks.append(
            Plot.axisX({"anchor": "top"}),  # type:ignore
        )
        marks.append(
            Plot.raster(  # type:ignore
                raster_xda.values.reshape(-1).tolist(),
                {
                    "width": raster_width,
                    "height": raster_height,
                    "imageRendering": "pixelated",
                },
            ),
        )

        marks.extend(self.build_marks())

        style = {}
        if dark_mode:
            style.update(
                {
                    "backgroundColor": "#111111",
                    "color": "#eeeeee",
                }
            )

        # Note: height seems to break aspectRatio
        # whereas width does not, hence it is kept.
        # The best way for a pixel-perfect display is margin=0
        # + defining the width and height manually
        margin_right = kwargs.get("marginRight", 0)
        margin_left = kwargs.get("marginLeft", 0)
        width_with_margins = width * scale + margin_right + margin_left

        # Note that by default the y-axis is descending.
        default_kwargs = {
            "width": width_with_margins,
            "color": {"scheme": "magma"},
            "x": {"domain": [0, raster_width], "label": "column"},
            "y": {"domain": [raster_height, 0], "label": "row"},
            "marks": marks,
            "style": style,
            "aspectRatio": 1,
        }
        initial_kwargs = self.initial_kwargs
        merged_kwargs = {**default_kwargs, **initial_kwargs, **kwargs}
        return op_instance(merged_kwargs)  # type:ignore


def build_base_xarray_plot(
    xda: xr.DataArray,
    callback: Callable[[list[Any]], None],
    *,
    dark_mode: bool = True,
    scale: float = 1,
    width: int = 140 * 4,
    do_convert_ascii_array_to_uint8: bool = True,
    **kwargs: Any,
) -> Obsplot:
    # Callback is a consumer of list of marks that enrich it.

    grid = xda
    if do_convert_ascii_array_to_uint8:
        grid = (grid == ord("#")).astype(int) * 255

    marks = []
    marks.append(
        Plot.axisX({"anchor": "top"}),  # type:ignore
    )

    marks.append(
        Plot.raster(  # type:ignore
            grid.values.reshape(-1).tolist(),
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

    mr = kwargs.get("marginRight", 0)
    ml = kwargs.get("marginLeft", 0)
    return op_instance(  # type:ignore
        {
            **{
                # weight seems to break aspectRatio
                # whereas width does not, hence it is kept.
                # "height": 140 * 4 * scale,
                "width": width * scale + mr + ml,
                "color": {"scheme": "magma"},
                "x": {"domain": [0, grid.col.size], "label": "column"},
                "y": {"domain": [grid.row.size, 0], "label": "row"},
                "marks": marks,
                "style": style,
                "aspectRatio": 1,
            },
            **kwargs,
        }
    )
