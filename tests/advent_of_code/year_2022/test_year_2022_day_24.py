import matplotlib.pyplot as plt
import numpy as np

from advent_of_code.year_2022.year_2022_day_24 import (
    advance_blizzard,
    compute_simulation_for_cross_period,
    initialize_blizzard,
    parse_text_input,
)

EXAMPLE_INPUT_DUMMY = """

#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#

"""


EXAMPLE_INPUT = """

#E######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#

"""


def test_year_2022_day_24_part_1_period_dummy():
    test_input = EXAMPLE_INPUT_DUMMY
    parsed_input = parse_text_input(test_input)
    blizzard = initialize_blizzard(parsed_input)
    initial_blizzard_backup = blizzard.copy(deep=True)
    for i in range(blizzard.row.size * blizzard.col.size):
        print(i)
        advance_blizzard(blizzard)
    assert np.all(sum(initial_blizzard_backup.values()) == sum(blizzard.values()))
    assert all(v for v in np.all(initial_blizzard_backup == blizzard).values())


def test_year_2022_day_24_part_1_period():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    blizzard = initialize_blizzard(parsed_input)
    initial_blizzard_backup = blizzard.copy(deep=True)
    for i in range(blizzard.row.size * blizzard.col.size):
        print(i)
        advance_blizzard(blizzard)
    assert np.all(sum(initial_blizzard_backup.values()) == sum(blizzard.values()))
    assert all(v for v in np.all(initial_blizzard_backup == blizzard).values())


def test_year_2022_day_24_part_1_period_stack():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    blizzard_cube = compute_simulation_for_cross_period(parsed_input)

    # See https://matplotlib.org/stable/gallery/mplot3d/voxels.html
    # Also See https://matplotlib.org/stable/gallery/mplot3d/voxels_rgb.html

    # prepare some coordinates
    x, y, z = (
        blizzard_cube.time.values,
        blizzard_cube.col.values,
        blizzard_cube.row.values,
    )

    # draw cuboids in the top left and bottom right corners, and a link between
    # them
    # cube1 = (x < 3) & (y < 3) & (z < 3)
    # cube2 = (x >= 5) & (y >= 5) & (z >= 5)
    # link = abs(x - y) + abs(y - z) + abs(z - x) <= 2

    # combine the objects into a single boolean array
    # voxelarray = cube1 | cube2 | link
    voxelarray = np.bool_(
        sum(blizzard_cube.values()).transpose("time", "col", "row").values
    )

    # focus on path
    show_negative = True
    if show_negative:
        voxelarray = ~voxelarray
    # voxelarray = blizzard_cube.right.values
    # set the colors of each object
    colors = np.empty(voxelarray.shape, dtype=object)
    colors[voxelarray] = "blue"

    # and plot everything
    ax = plt.figure().add_subplot(projection="3d")
    ax.voxels(voxelarray, facecolors=colors, edgecolor="k")
    ax.set(xlabel="time", ylabel="col", zlabel="row")
    ax.invert_yaxis()
    ax.invert_zaxis()
    ax.set_aspect("equal")
    plt.show()
    # # prepare some coordinates
    # x, y, z = np.indices((8, 8, 8))

    # # draw cuboids in the top left and bottom right corners, and a link between
    # # them
    # cube1 = (x < 3) & (y < 3) & (z < 3)
    # cube2 = (x >= 5) & (y >= 5) & (z >= 5)
    # link = abs(x - y) + abs(y - z) + abs(z - x) <= 2

    # # combine the objects into a single boolean array
    # voxelarray = cube1 | cube2 | link

    # # set the colors of each object
    # colors = np.empty(voxelarray.shape, dtype=object)
    # colors[link] = "red"
    # colors[cube1] = "blue"
    # colors[cube2] = "green"

    # # and plot everything
    # ax = plt.figure().add_subplot(projection="3d")
    # ax.voxels(voxelarray, facecolors=colors, edgecolor="k")

    # plt.show()

    ...


def test_year_2022_day_24_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    blizzard_cube = compute_simulation_for_cross_period(parsed_input)
    # Do recursive exploration!
    assert minutes == 18
    ...


def test_year_2022_day_24_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    ...
