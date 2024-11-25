from dataclasses import dataclass, field, replace
from typing import Any, Callable, Iterable, Literal, Self, override

import numpy as np
import pandas as pd
import xarray as xr
from pyobsplot import Obsplot, Plot
from pyobsplot.widget import ObsplotWidget

from advent_of_code.y_2023.problem_202311 import get_compartiments

MarkProducerSignature = Callable[[], list[Any]]


def create_obsplot_instance(
    *,
    format: Literal["widget", "html", "svg", "png"] = "html",
    theme: Literal["current", "light", "dark"] = "dark",
    debug: bool = True,
):
    # See https://juba.github.io/pyobsplot/usage.html#renderers
    return Obsplot(format, theme=theme, debug=debug)


# This is a singleton instance of observable plot, allowing further customization like
# changing the renderer from 'widget' to 'json'.

op_instance = create_obsplot_instance(format="html", theme="current")


def create_marks_puzzle_input_202311(
    space_xda: xr.DataArray,
    *,
    with_rules: bool = False,
    with_graph: bool = False,
    coord_array: xr.DataArray | None = None,
    edge_density: float | None = None,
    with_chunk_graph: bool = False,
) -> MarkProducerSignature:
    def callback() -> list[Any]:
        marks = []

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

        return marks

    return callback


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
            rows = [idx[0] + 0.5 for idx in df.index]  # type: ignore
            cols = [idx[1] + 0.5 for idx in df.index]  # type: ignore
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
        # Plot.text(  # type:ignore
        #     lines_df,
        #     {
        #         **{
        #             x_target: lines_df["x2"].to_list(),
        #             y_target: lines_df["y2"].to_list(),
        #             "tickFormat": ".0s",
        #             "fill": "currentColor",
        #             "stroke": "black",
        #             "dy": -12,
        #         },
        #     },
        # ),
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

    style = {}
    style.update(
        {
            "backgroundColor": "#111111",
            "color": "#eeeeee",
        }
    )

    return op_instance(  # type: ignore
        # return op_instance_dark(  # type: ignore
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
            style=style,
        )
    )


@dataclass(kw_only=True, frozen=True)
class ObservablePlotBuilder:
    _marks_producers: list[MarkProducerSignature] = field(default_factory=list)
    _op: Obsplot = op_instance
    initial_kwargs: dict[str, Any]

    def copy(self, **kwargs: Any) -> Self:
        # For convenience, allow to alter the initial_kwargs when copying.
        # Any passed kwarg will override any existing one on the original builder.
        updated_kwargs = {**self.initial_kwargs, **kwargs}
        return replace(
            self,
            initial_kwargs=updated_kwargs,
            _marks_producers=[*self._marks_producers],
        )

    def build_marks(self) -> list[Any]:
        marks = []
        for marks_producer in self._marks_producers:
            produced_marks = marks_producer()
            marks.extend(produced_marks)
        return marks

    def prepend(self, mark_producer: MarkProducerSignature) -> Self:
        self._marks_producers.insert(0, mark_producer)
        return self

    def insert(self, mark_producer: MarkProducerSignature, index: int) -> Self:
        self._marks_producers.insert(index, mark_producer)
        return self

    def append(self, mark_producer: MarkProducerSignature) -> Self:
        self._marks_producers.append(mark_producer)
        return self

    def extend(self, mark_producers: Iterable[MarkProducerSignature]) -> Self:
        self._marks_producers.extend(mark_producers)
        return self

    def stack(self, mark_producer: MarkProducerSignature) -> Self:
        self.append(mark_producer)
        return self

    def unstack(self, index: int = -1) -> Self:
        self.pop(index)
        return self

    def pop(self, index: int = -1) -> MarkProducerSignature:
        return self._marks_producers.pop(index)

    def plot(self, **kwargs: Any) -> Obsplot:
        # Priority:
        # Initial kwargs passed on builder creation,
        # overridable by kwargs in this method call,
        # and finally the marks is built in this method.
        merged_kwargs = {
            **self.initial_kwargs,
            **kwargs,
            **dict(marks=self.build_marks()),
        }
        return self._op(merged_kwargs)  # type:ignore


@dataclass(kw_only=True, frozen=True)
class ObservablePlotXarrayBuilder(ObservablePlotBuilder):
    raster_xda: xr.DataArray

    @property
    def raster_width(self) -> int:
        return self.raster_xda["col"].size

    @property
    def raster_height(self) -> int:
        return self.raster_xda["row"].size

    def __post_init__(self):
        marks = self.create_raster_background_marks()
        self.prepend(marks)

    @override
    def copy(self, *, raster_xda: xr.DataArray | None = None, **kwargs: Any) -> Self:
        # This code is inefficient as it can create two raster layers for no use...
        new_builder = super().copy(**kwargs)
        new_builder.unstack(
            1
        )  # Remove old raster background, now in second position in the layers
        if raster_xda is None:
            return new_builder

        replaced = replace(new_builder, raster_xda=raster_xda)
        replaced.unstack(
            1
        )  # Remove old raster background, now in second position in the layers
        return replaced

    @override
    def plot(self, **kwargs: Any) -> Obsplot:
        verbose: bool = self.initial_kwargs.get("verbose", True)
        dark_mode: bool = self.initial_kwargs.get("dark_mode", True)
        scale: float = self.initial_kwargs.get("scale", 1)
        width: int = self.initial_kwargs.get("width", 140 * 4)
        height: int = self.initial_kwargs.get("height", None)
        ascending_y_axis = self.initial_kwargs.get("ascending_y_axis", False)
        legend: bool = self.initial_kwargs.get("legend", False)
        marks = self.build_marks()

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
        margin = self.initial_kwargs.get("margin", 0)
        margin_right = self.initial_kwargs.get("marginRight", margin)
        margin_left = self.initial_kwargs.get("marginLeft", margin)
        margin_top = self.initial_kwargs.get("marginTop", margin)
        margin_bottom = self.initial_kwargs.get("marginBottom", margin)
        width_with_margins = width * scale + margin_right + margin_left
        height_with_margins = (
            (height * scale + margin_top + margin_bottom) if height else None
        )
        if height_with_margins is None:
            if verbose:
                print("Warning: potential issue with no given height")
        label = self.initial_kwargs.get("label", False)

        # Note that by default the y-axis is descending.
        # It can be changed via kwarg 'ascending_y_axis'
        x_domain = [0, self.raster_width]
        y_domain = [0, self.raster_height]

        default_kwargs = {
            "color": {"scheme": "magma", "legend": legend},
            "x": {
                "domain": x_domain,
                "label": "column" if label else None,
                "ticks": self.initial_kwargs.pop("x_ticks", None),
            },
            "y": {
                "domain": y_domain if ascending_y_axis else list(reversed(y_domain)),
                "label": "row" if label else None,
                "ticks": self.initial_kwargs.pop("y_ticks", None),
            },
            "marks": marks,
            "style": style,
            "aspectRatio": 1,
        }
        merged_kwargs = {
            **default_kwargs,
            **self.initial_kwargs,
            **{
                "width": width_with_margins,
                "height": height_with_margins,
            },
            **kwargs,
        }
        if verbose:
            for idx, mark_producer in enumerate(self._marks_producers):
                print(f"Layer #{idx}", mark_producer)
        # if verbose:
        # print(merged_kwargs)
        return self._op(merged_kwargs)  # type: ignore

    def create_raster_background_marks(self) -> MarkProducerSignature:
        def callback() -> list[Any]:
            marks = []

            marks.append(
                Plot.axisX({"anchor": "top"}),  # type:ignore
            )
            marks.append(
                Plot.raster(  # type:ignore
                    self.raster_xda.values.reshape(-1).tolist(),
                    {
                        "width": self.raster_width,
                        "height": self.raster_height,
                        "imageRendering": "pixelated",
                    },
                ),
            )

            return marks  # type:ignore

        return callback


def build_base_xarray_plot(
    xda: xr.DataArray,
    callback: Callable[[list[Any]], None],
    *,
    dark_mode: bool = True,
    scale: float = 1,
    width: int = 140 * 4,
    do_convert_ascii_array_to_uint8: bool = True,
    **kwargs: Any,
) -> ObsplotWidget | None:
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
    path = kwargs.pop("path", None)
    plot = op_instance(  # type:ignore
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
        },
        path=path,
    )
    # if plot is None:
    # raise RuntimeError("plot instanciation failed (is None)")
    return plot


def create_polygon_layer(
    links_df: pd.DataFrame,
    *,
    color: str = "red",
    stroke_width: int = 2,
    offset: float = 0,
    x1_target: str = "x1",
    x2_target: str = "x2",
    y1_target: str = "y1",
    y2_target: str = "y2",
) -> Callable[[], list[Any]]:
    def callback() -> list[Any]:
        return [
            Plot.link(  # type:ignore
                links_df + offset,
                {
                    x1_target: "x1",
                    y1_target: "y1",
                    x2_target: "x2",
                    y2_target: "y2",
                    "stroke": color,
                    "strokeWidth": stroke_width,
                    "markerEnd": "arrow",
                },
            )
        ]

    return callback


def create_indicative_dots_layer(
    raster_xda: xr.DataArray,
    *,
    radius: int = 100,
    color: str = "white",
    opacity: float = 1,
    highlight_origin: bool = False,
) -> Callable[[], list[Any]]:
    def callback() -> list[Any]:
        offset = 1
        data = np.zeros(
            (
                raster_xda.shape[0] + offset,
                raster_xda.shape[1] + offset,
            ),
            dtype=int,
        )
        xda_with_borders = xr.DataArray(
            data=data,
            dims=("row", "col"),
            coords=dict(
                row=np.arange(data.shape[0]),
                col=np.arange(data.shape[1]),
            ),
        )
        xda = xda_with_borders
        # Convert a MultiIndex to a DataFrame:
        # See https://pandas.pydata.org/docs/reference/api/pandas.MultiIndex.to_frame.html
        df = xda.stack({"z": ("row", "col")}).to_pandas().index.to_frame()
        marks = [
            Plot.dot(  # type:ignore
                df,
                {"x": "col", "y": "row", "color": color, "opacity": 0.05, "r": radius},
            ),
            Plot.dot(  # type:ignore
                df,
                {
                    "x": "col",
                    "y": "row",
                    "color": color,
                    "opacity": opacity,
                    "r": radius // 4,
                },
            ),
            Plot.dot(  # type:ignore
                df,
                {
                    "x": "col",
                    "y": "row",
                    "color": color,
                    "opacity": opacity,
                    "r": radius,
                    "symbol": "square",
                },
            ),
        ]
        if highlight_origin:
            new_marks = [
                # Origin at (0, 0)
                Plot.dot(  # type:ignore
                    [(0, 0)], {"stroke": "#0f0", "r": radius}
                ),
                # Origin at (0, 0)
                Plot.dot(  # type:ignore
                    [(0, 0)], {"stroke": "#0f0", "r": radius // 4}
                ),
            ]

            marks.extend(new_marks)
        return marks

    return callback


def create_boundary_points_layer(
    boundary_points_coords: pd.DataFrame,
    *,
    with_discs: bool = True,
    x_name: str = "x",
    y_name: str = "y",
    **kwargs: Any,
) -> Callable[[], list[Any]]:
    def callback() -> list[Any]:
        marks = []
        marks.append(
            Plot.dot(  # type:ignore
                boundary_points_coords,
                {"x": x_name, "y": y_name, "stroke": "stroke", **kwargs},
            ),
        )
        if with_discs:
            marks.append(
                Plot.dot(  # type:ignore
                    boundary_points_coords,
                    {
                        "x": x_name,
                        "y": y_name,
                        "stroke": "stroke",
                        **kwargs,
                        "r": kwargs["r"] // 4,
                        "symbol": "disc",
                        "strokeWidth": 2,
                    },
                )
            )
        return marks

    return callback


# Based on visualize_puzzle_input_202310
def text_mark_producer(
    xda: xr.DataArray,
    *,
    text_xda: xr.DataArray | None = None,
    width: int,
) -> Callable[[], list[Any]]:
    def callback() -> list[Any]:
        if text_xda is None:
            return []

        df = text_xda.stack(z=("row", "col")).to_pandas()
        data = df.values.tolist()
        rows = [idx[0] + 0.5 for idx in df.index]  # type: ignore
        cols = [idx[1] + 0.5 for idx in df.index]  # type: ignore
        return [
            Plot.text(  # type:ignore
                data,
                {
                    "text": Plot.identity,  # type: ignore
                    "x": cols,
                    "y": rows,
                    "color": "white",
                    "fontSize": 38 * width / 600 * 13 / xda["col"].size,
                },
            )
        ]

    return callback


def ascii_2d_numpy_array_plotter(
    xda: xr.DataArray,
    *,
    obfuscate: bool = True,
    text: bool = True,
    scheme: str = "Tableau10",
    legend: bool = True,
    **kwargs: Any,
) -> ObservablePlotXarrayBuilder:
    if xda.dtype == np.uint8:
        simplified_xda = xda.where(
            ~xda.isin(list(range(ord("1"), ord("9") + 1))), ord("N")
        )
    else:
        simplified_xda = xda

    text_xda = None

    if text:
        if obfuscate:
            text_xda = simplified_xda
        else:
            text_xda = xda

        if text_xda.dtype != np.dtype("<U1"):
            # Convert ASCII uint8 to str (S1) then str (for it to be serializable)
            text_xda = text_xda.copy(data=text_xda.values.view("S1").astype("str"))

    if xda.dtype == np.uint8:
        simplified_xda = simplified_xda.copy(
            data=simplified_xda.values.view("S1").astype("str")
        )
    kwargs = {
        **dict(
            margin=0,
            do_convert_ascii_array_to_uint8=False,
            color={"type": "categorical", "scheme": scheme, "legend": legend},
        ),
        **kwargs,
    }

    plotter = ObservablePlotXarrayBuilder(
        raster_xda=simplified_xda, initial_kwargs=kwargs
    )
    text_callback = text_mark_producer(
        simplified_xda, text_xda=text_xda, width=kwargs["width"]
    )
    plotter.stack(text_callback)

    return plotter
