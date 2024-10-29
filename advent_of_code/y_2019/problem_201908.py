from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt
from advent_of_code.common.protocols import AdventOfCodeProblem
import xarray as xr

type PuzzleInput = npt.NDArray[np.integer[Any]]


@dataclass(kw_only=True)
class AdventOfCodeProblem201908(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2019
    day: int = 8

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return np.array(list((map(int, list(text.strip())))))

    def solve_part_1(self, puzzle_input: PuzzleInput):
        image_layers_xda = xr.DataArray(
            puzzle_input.reshape((-1, 6, 25)), dims=("layer", "row", "col")
        )
        counts = [(image_layers_xda == i).sum(dim=["row", "col"]) for i in range(3)]
        idx = np.argmin(counts[0].data)  # index_of_layer_with_fewest_0_digits
        res = (counts[1][idx] * counts[2][idx]).item()
        return res

    def solve_part_2(self, puzzle_input: PuzzleInput):
        image_layers_xda = xr.DataArray(
            puzzle_input.reshape((-1, 6, 25)), dims=("layer", "row", "col")
        )
        indices = np.array(
            [
                np.argmax(image_layers_xda.data.reshape((-1, 6 * 25))[:, i] != 2)
                for i in range(6 * 25)
            ]
        )
        filtered = np.array(
            [
                image_layers_xda.data.reshape((-1, 6 * 25))[indices[i], i]
                for i in range(6 * 25)
            ]
        ).reshape((6, 25))
        print(
            "\n".join(
                "".join("#" if cell == 1 else " " for cell in row) for row in filtered
            )
        )
        return -1  # TODO read the message


if __name__ == "__main__":
    print(AdventOfCodeProblem201908().solve())
