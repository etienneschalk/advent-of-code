import os
from typing import Literal


def attempt_interactive(
    i_want_interactive_plots: bool,
    backend: Literal["plotly", "hvplot"],
    renderer_interactive: str = "vscode",
    renderer_static: str = "svg",
):
    # See https://github.com/microsoft/vscode-jupyter/issues/6999
    # pio.renderers.default = "plotly_mimetype+notebook"

    i_am_in_vscode = os.environ.get("VSCODE_PID") is not None
    interactive = i_am_in_vscode and i_want_interactive_plots
    if backend == "plotly":
        import plotly.io as pio

        # Unfortunately the dynamic rendering of plotly does not work on GitHub Pages.
        # The following falls back on rendering static images (SVG)
        if interactive:
            pio.renderers.default = renderer_interactive
        else:
            pio.renderers.default = renderer_static
        print(f"Plotly will render to {pio.renderers.default=}")

    elif backend == "hvplot":
        import hvplot

        # Unfortunately the dynamic rendering of hvplot does not work on GitHub Pages.
        # The following falls back on rendering static images with matplotlib
        if interactive:
            print(f"{backend} will render interactive plots")
        else:
            hvplot.extension("matplotlib")  # type: ignore
            print(f"{backend} will render static plots using matplotlib")

    else:
        raise NotImplementedError
