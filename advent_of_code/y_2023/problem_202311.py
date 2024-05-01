from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt
import xarray as xr

from advent_of_code.common.common import parse_2d_string_array_to_uint8_xarray
from advent_of_code.y_2023.problem_202301 import AdventOfCodeProblem

type PuzzleInput = xr.DataArray


@dataclass(kw_only=True)
class AdventOfCodeProblem202311(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 11

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)

    def solve_part_1_naive(self, puzzle_input: PuzzleInput):
        expanded_space = expand_space(puzzle_input)
        proximity_matrix = compute_proximity_matrix(expanded_space)
        result = compute_sum_of_shortest_paths_between_pairs(proximity_matrix)
        return result

    def solve_part_1(self, puzzle_input: PuzzleInput):
        # idempotence part 1 part 2
        naive_result = self.solve_part_1_naive(puzzle_input)
        result = compute_sum_of_shortest_paths_part_2(puzzle_input, 1)
        assert naive_result == result
        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        # Do not expand space manually
        result = compute_sum_of_shortest_paths_part_2(
            puzzle_input, get_expansion_coef_part_2()
        )
        return result


def get_expansion_coef_part_2() -> int:
    return 1000000 - 1


def compute_sum_of_shortest_paths_part_2(
    space_xda: xr.DataArray, expansion_coef: int
) -> int:
    """Compute sum of shortest paths for Part 2

    The trick is to apply the same logic to both stars, and chunks.
    The first "star matrix" contains the distance between stars, without expansion.
    The second "chunk matrix" contains the distance between the chunks they are being a part of.
    The two matrices have the same shape, and can be added together, with the "chunk matrix"
    being multiplied by the expansion factor scalar.

    Parameters
    ----------
    space_xda
        Array containing stars
    expansion_coef
        Expansion coefficient

    Returns
    -------
        The sum of shortest paths
    """
    coord_array = create_coord_array(space_xda)
    chunk_coord_array = create_chunk_coord_array(space_xda, coord_array)

    proximity_matrix_stars = compute_proximity_matrix_from_coord_array(coord_array)
    proximity_matrix_chunks = compute_proximity_matrix_from_coord_array(
        chunk_coord_array
    )

    total_proximity = proximity_matrix_stars + expansion_coef * proximity_matrix_chunks
    result = compute_sum_of_shortest_paths_between_pairs(total_proximity)
    return result


def compute_sum_of_shortest_paths_between_pairs(proximity_matrix: xr.DataArray) -> int:
    return np.triu(proximity_matrix).sum()


def create_coord_array(space_xda: xr.DataArray) -> xr.DataArray:
    # From the space matrix, compute pairs of stars' coordinates
    stacked = (space_xda == ord(b"#")).stack(z=("row", "col"), create_index=False)
    indices = stacked[stacked]
    coord_array = xr.DataArray(
        np.array([indices.row, indices.col]),
        dims=("idx", "z"),
        coords={"idx": ["row", "col"]},
    ).T

    return coord_array


def create_chunk_coord_array(
    space_xda: xr.DataArray, coord_array: xr.DataArray
) -> xr.DataArray:
    row_chunks = get_compartiments(space_xda, "row", "col")
    col_chunks = get_compartiments(space_xda, "col", "row")

    chunk_coords: list[list[int]] = []
    for z in coord_array.z:
        row, col = coord_array.isel(z=z)
        chunk_row = find_compartiment_id(row, row_chunks)
        chunk_col = find_compartiment_id(col, col_chunks)
        chunk_coords.append([chunk_row, chunk_col])
    chunk_coord_array = coord_array.copy(data=chunk_coords)
    return chunk_coord_array


def compute_proximity_matrix_from_coord_array(
    coord_array: xr.DataArray,
) -> xr.DataArray:
    """Compute proximity matrix from coordinates array

    Parameters
    ----------
    coord_array
        Array containing coordinates of the graph nodes (stars)

    Returns
    -------
        Proximity matrix: Pair-wise distance of nodes

    Notes
    -----
    425*425 = 180625 -> this operation is O(n**2) with n=425
    This is because for each node, the distance to all its peers must be computed
    This is
    An optimization would be to only compute the triangular par of the matrix
    (2 among n) = n(n-1) / 2  (edge count in graphe complet)
    -> but still O(n)
    """

    print("compute_proximity_matrix_from_coord_array start")

    array_list = [
        abs(coord_array.isel(z=i) - coord_array).sum(dim="idx")
        for i in coord_array["z"]
    ]

    proximity_matrix = xr.concat(array_list, dim="z2")

    print("compute_proximity_matrix_from_coord_array end")

    return proximity_matrix


def compute_proximity_matrix(space_xda: xr.DataArray) -> xr.DataArray:
    """Compute proximity matrix

    First, coordinates of each star are gathered.
    Then, the matrix of Manhattan distances between each of them is returned

    Parameters
    ----------
    space_xda
        Data Array representing stars

    Returns
    -------
        Proximity matrix

    Notes
    -----
    This way of storing distance between stars is inspired from the
    "Adjacency matrix" concept from graph theory.

    See `Adjacency matrix on Wikipédia <https://en.wikipedia.org/wiki/proximity_matrix/>`_.

    """
    coord_array = create_coord_array(space_xda)
    proximity_matrix = compute_proximity_matrix_from_coord_array(coord_array)
    return proximity_matrix


def expand_space(parsed_input: xr.DataArray) -> xr.DataArray:
    xda = parsed_input
    xda = pad_xda(xda, "col", "row")
    xda = pad_xda(xda, "row", "col")
    return xda


def get_compartiments(
    xda: xr.DataArray, chunks_dim: str, dim_reduce: str
) -> dict[int, range]:
    offset = (xda == ord(b".")).all(dim=dim_reduce)
    cs = offset[offset][chunks_dim] + 1
    boundaries: npt.NDArray[np.int64] = np.pad(
        cs, (1, 1), constant_values=(0, len(offset))
    )

    ranges = [
        range(boundaries[i], boundaries[i + 1]) for i in range(len(boundaries) - 1)
    ]
    compartiments = {idx: v for idx, v in enumerate(ranges)}
    return compartiments


def find_compartiment_id(value: int, compartiments: dict[int, range]) -> int:
    # This is extremely inefficient.
    for k, v in compartiments.items():
        if v.start <= value < v.stop:
            return k
    raise ValueError


def pad_xda(xda: xr.DataArray, dim_reduce: str, dim_concat: str) -> xr.DataArray:
    # Note: Unpacking a dict into the kwargs of sel seems not to work well with typing
    # (only an Any-typed variable is accepted)
    # Note: xr.concat also requires the same pyright ignore directive.
    i = 0
    to_concat: list[xr.DataArray] = []
    to_insert = (xda == ord(b".")).all(dim=dim_reduce)
    for index in to_insert[to_insert][dim_concat]:
        # contravariance in kwargs?? slice is not acceptable as an Any
        slice_i_index_any: Any = slice(i, index)
        to_concat.append(
            xda.sel(  # pyright: ignore[reportUnknownMemberType]
                **{dim_concat: slice_i_index_any}
            )
        )
        to_concat.append(
            xda.sel(**{dim_concat: index})  # pyright: ignore[reportUnknownMemberType]
        )
        i = index + 1
    slice_i_none_any: Any = slice(i, None)
    to_concat.append(
        xda.sel(  # pyright: ignore[reportUnknownMemberType]
            **{dim_concat: slice_i_none_any}
        )
    )
    concatenated = xr.concat(  # pyright: ignore[reportUnknownMemberType]
        to_concat, dim=dim_concat
    )
    dim_concat_value_any: Any = list(range(len(concatenated[dim_concat])))
    return concatenated.assign_coords(  # pyright: ignore[reportUnknownMemberType]
        **{dim_concat: dim_concat_value_any}
    )


def parse_text_input(text: str) -> PuzzleInput:
    return parse_2d_string_array_to_uint8_xarray(text)


if __name__ == "__main__":
    print(AdventOfCodeProblem202311().solve())
