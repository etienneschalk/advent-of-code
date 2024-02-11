from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2023.year_2023_day_03 import (
    find_part_numbers,
    find_part_numbers_and_gears,
    parse_text_input,
)


def test_year_2023_day_3_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    array = parse_text_input(test_input)

    flattened = find_part_numbers(array)

    assert flattened == [467, 35, 633, 617, 592, 755, 664, 598]
    assert 114 not in flattened
    assert 58 not in flattened
    assert sum(flattened) == 4361


def test_year_2023_day_3_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    array = parse_text_input(test_input)

    gear_part_numbers_tuples = find_part_numbers_and_gears(array)

    assert gear_part_numbers_tuples == [(467, 35), (755, 598)]

    gear_ratios = [t[0] * t[1] for t in gear_part_numbers_tuples]

    assert gear_ratios[0] == 16345
    assert gear_ratios[1] == 451490

    sum_of_gear_ratios = sum(gear_ratios)

    assert sum_of_gear_ratios == 467835
