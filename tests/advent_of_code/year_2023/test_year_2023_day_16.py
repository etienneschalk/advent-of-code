import numpy as np

from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2023.year_2023_day_16 import (
    MOVE_EAST,
    MOVE_SOUTH,
    Beam,
    do_part_1,
    do_part_2,
    parse_text_input,
    render_parsed_input,
)


def test_year_2023_day_16_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    print()
    print(render_parsed_input(parsed_input))
    initial_beam = Beam(np.array((1, 0)), MOVE_EAST)
    assert do_part_1(parsed_input, initial_beam=initial_beam, max_depth=31) == 45
    assert do_part_1(parsed_input, initial_beam=initial_beam, max_depth=32) == 46
    assert do_part_1(parsed_input, initial_beam=initial_beam, max_depth=33) == 46
    ...


def test_year_2023_day_16_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    print()
    print(render_parsed_input(parsed_input))
    initial_beam = Beam(np.array((0, 4)), MOVE_SOUTH)
    assert do_part_1(parsed_input, initial_beam=initial_beam, max_depth=32) == 49
    assert do_part_1(parsed_input, initial_beam=initial_beam, max_depth=33) == 50
    assert do_part_1(parsed_input, initial_beam=initial_beam, max_depth=34) == 51
    assert do_part_1(parsed_input, initial_beam=initial_beam, max_depth=35) == 51

    assert do_part_2(parsed_input, max_depth=32) == 49
    assert do_part_2(parsed_input, max_depth=33) == 50
    assert do_part_2(parsed_input, max_depth=34) == 51
    assert do_part_2(parsed_input, max_depth=35) == 51
    ...
