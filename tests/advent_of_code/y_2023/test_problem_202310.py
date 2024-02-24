import numpy as np
import pytest
import xarray as xr

from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202310 import (
    AdventOfCodeProblem202310,
    parse_text_input,
    render_2d_array_to_text,
)


def test_problem_202310_part_1(example_inputs_2023: ExampleInputsStore):
    test_inputs = (
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_1_1"),
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_1_2"),
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_1_3"),
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_2_1"),
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_2_2"),
    )
    parsed_inputs = [parse_text_input(test_input) for test_input in test_inputs]
    for p in parsed_inputs:
        print(render_2d_array_to_text(p))

    minimum_distances = AdventOfCodeProblem202310().compute_minimum_distances(
        parsed_inputs[1]
    )
    result = np.max(minimum_distances)
    print(render_2d_array_to_text(minimum_distances))
    assert result == 4

    minimum_distances = AdventOfCodeProblem202310().compute_minimum_distances(
        parsed_inputs[2]
    )
    result = np.max(minimum_distances)
    print(render_2d_array_to_text(minimum_distances))
    assert result == 4

    minimum_distances = AdventOfCodeProblem202310().compute_minimum_distances(
        parsed_inputs[3]
    )
    result = np.max(minimum_distances)
    print(render_2d_array_to_text(minimum_distances))
    assert result == 8

    minimum_distances = AdventOfCodeProblem202310().compute_minimum_distances(
        parsed_inputs[4]
    )
    result = np.max(minimum_distances)
    print(render_2d_array_to_text(minimum_distances))
    assert result == 8


@pytest.mark.skip(reason="_fill_macro_pixel_first_try not available anymore")
def test_problem_202310_part_2(example_inputs_2023: ExampleInputsStore):
    test_inputs = (
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_PART_2_1_1a"),
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_PART_2_1_1b"),
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_PART_2_1_2"),
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_PART_2_2_1"),
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_PART_2_2_2"),
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_PART_2_3_1"),
        example_inputs_2023.retrieve(__file__, "EXAMPLE_INPUT_PART_2_3_2"),
    )

    parsed_inputs = [parse_text_input(test_input) for test_input in test_inputs]
    for p in parsed_inputs:
        print(render_2d_array_to_text(p))
        minimum_distances = AdventOfCodeProblem202310().compute_minimum_distances(p)
        print(render_2d_array_to_text(minimum_distances))

    maze = parsed_inputs[2]
    minimum_distances = AdventOfCodeProblem202310().compute_minimum_distances(maze)
    import numpy as np

    contours = np.int32(np.bool_(minimum_distances))
    rolled_i = np.roll(contours, 1, axis=0)
    rolled_j = np.roll(contours, 1, axis=1)
    print(render_2d_array_to_text(np.roll(contours, 1, axis=1)))
    assert np.all(np.cumsum((contours - rolled_i), axis=0) == contours)
    assert np.all(np.cumsum((contours - rolled_j), axis=1) == contours)

    main_loop = np.where(minimum_distances != 0, maze, "░")
    print(render_2d_array_to_text(main_loop))
    arr = minimum_distances
    arr_2x = np.zeros(2 * np.array(arr.shape), dtype=np.bool_)
    # Ignore padded contour (1px)
    for i in range(1, arr.shape[0] - 1):
        for j in range(1, arr.shape[1] - 1):
            ...
            # _fill_macro_pixel_first_try(main_loop, arr_2x, i, j)
    ...
    _ = arr_2x
    print(render_2d_array_to_text(arr_2x))
    xda = (
        xr.DataArray(arr_2x, dims=("i", "j"))
        .coarsen(i=2, j=2)
        .sum()  # pyright: ignore[reportGeneralTypeIssues]
    )
    print(render_2d_array_to_text(xda.data))

    ...
