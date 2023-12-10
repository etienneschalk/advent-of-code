import xarray as xr

from advent_of_code.year_2023.year_2023_day_10 import (
    fill_macro_pixel,
    logic_part_1,
    parse_text_input,
    render_2d_array_to_text,
)

EXAMPLE_INPUT_1_1 = """
.....
.F-7.
.|.|.
.L-J.
.....
"""
EXAMPLE_INPUT_1_2 = """
.....
.S-7.
.|.|.
.L-J.
.....
"""
EXAMPLE_INPUT_1_3 = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

EXAMPLE_INPUT_2_1 = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
EXAMPLE_INPUT_2_2 = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

EXAMPLE_DISTANCES_1 = """
.....
.012.
.1.3.
.234.
.....
"""
EXAMPLE_DISTANCES_2 = """
..45.
.236.
01.78
14567
23...
"""


def test_year_2023_day_10_part_1():
    test_inputs = (
        EXAMPLE_INPUT_1_1,
        EXAMPLE_INPUT_1_2,
        EXAMPLE_INPUT_1_3,
        EXAMPLE_INPUT_2_1,
        EXAMPLE_INPUT_2_2,
    )
    parsed_inputs = [parse_text_input(test_input) for test_input in test_inputs]
    for p in parsed_inputs:
        print(render_2d_array_to_text(p))

    result, minimum_distances = logic_part_1(parsed_inputs[1])
    print(render_2d_array_to_text(minimum_distances))
    assert result == 4

    result, minimum_distances = logic_part_1(parsed_inputs[2])
    print(render_2d_array_to_text(minimum_distances))
    assert result == 4

    result, minimum_distances = logic_part_1(parsed_inputs[3])
    print(render_2d_array_to_text(minimum_distances))
    assert result == 8

    result, minimum_distances = logic_part_1(parsed_inputs[4])
    print(render_2d_array_to_text(minimum_distances))
    assert result == 8
    ...


EXAMPLE_INPUT_PART_2_1_1a = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

EXAMPLE_INPUT_PART_2_1_1b = """
...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
"""
EXAMPLE_INPUT_PART_2_1_2 = """
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
"""
EXAMPLE_INPUT_PART_2_1_TEST = """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
"""

EXAMPLE_INPUT_PART_2_2_1 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

EXAMPLE_INPUT_PART_2_2_2 = """
OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
"""

EXAMPLE_INPUT_PART_2_3_1 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

EXAMPLE_INPUT_PART_2_3_2 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


def test_year_2023_day_10_part_2():
    test_inputs = (
        EXAMPLE_INPUT_PART_2_1_1a,
        EXAMPLE_INPUT_PART_2_1_1b,
        EXAMPLE_INPUT_PART_2_1_2,
        EXAMPLE_INPUT_PART_2_2_1,
        EXAMPLE_INPUT_PART_2_2_2,
        EXAMPLE_INPUT_PART_2_3_1,
        EXAMPLE_INPUT_PART_2_3_2,
    )

    parsed_inputs = [parse_text_input(test_input) for test_input in test_inputs]
    for p in parsed_inputs:
        print(render_2d_array_to_text(p))
        _, minimum_distances = logic_part_1(p)
        print(render_2d_array_to_text(minimum_distances))

    maze = parsed_inputs[2]
    _, minimum_distances = logic_part_1(maze)
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
            fill_macro_pixel(main_loop, arr_2x, i, j)
    ...
    _ = arr_2x
    print(render_2d_array_to_text(arr_2x))
    xda = xr.DataArray(arr_2x, dims=("i", "j")).coarsen(i=2, j=2).sum()
    print(render_2d_array_to_text(xda.data))

    ...
