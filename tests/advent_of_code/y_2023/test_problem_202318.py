from advent_of_code.common.constants import DOWN, LEFT, RIGHT, UP
from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202318 import (
    compute_area,
    compute_internal_perimeter,
    compute_pick_polygon_area_formula,
    compute_polygon_coords,
    compute_shoelace_formula,
    parse_text_input_part_1,
    parse_text_input_part_2,
)


def test_problem_202318_part_1_basic(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_3_X_3_LOOP")
    # Sources
    # Visualization (spoilers)
    # See https://www.reddit.com/r/adventofcode/comments/
    # 18l2tap/2023_day_18_the_elves_and_the_shoemaker/
    # Shoelace formula https://en.wikipedia.org/wiki/Shoelace_formula
    # Pick's theorem https://en.wikipedia.org/wiki/Pick%27s_theorem
    dig_plan = parse_text_input_part_1(test_input)

    internal_perimeter = compute_internal_perimeter(dig_plan)
    assert internal_perimeter == 8

    coords = compute_polygon_coords(dig_plan)
    shoelace_interior_area = compute_shoelace_formula(coords)
    assert shoelace_interior_area == 4
    pick_area_including_exterior = compute_pick_polygon_area_formula(
        shoelace_interior_area, internal_perimeter + 4
    )
    assert pick_area_including_exterior == 9


def test_problem_202318_part_1_basic_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_3_X_4_LOOP")
    dig_plan = parse_text_input_part_1(test_input)

    internal_perimeter = compute_internal_perimeter(dig_plan)
    assert internal_perimeter == 10

    coords = compute_polygon_coords(dig_plan)
    shoelace_interior_area = compute_shoelace_formula(coords)
    assert shoelace_interior_area == 6
    pick_area_including_exterior = compute_pick_polygon_area_formula(
        shoelace_interior_area, internal_perimeter + 4
    )
    assert pick_area_including_exterior == 12


def test_problem_202318_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    dig_plan = parse_text_input_part_1(test_input)

    internal_perimeter = compute_internal_perimeter(dig_plan)
    assert internal_perimeter == 38

    coords = compute_polygon_coords(dig_plan)
    shoelace_interior_area = compute_shoelace_formula(coords)
    pick_area_including_exterior = compute_pick_polygon_area_formula(
        shoelace_interior_area, internal_perimeter + 4
    )
    assert pick_area_including_exterior == 62


def test_problem_202318_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    dig_plan = parse_text_input_part_2(test_input)

    mapping = {
        RIGHT: "R",
        DOWN: "D",
        LEFT: "L",
        UP: "U",
    }
    expected_directions_list = [
        "R",
        "D",
        "R",
        "D",
        "R",
        "D",
        "L",
        "U",
        "L",
        "D",
        "L",
        "U",
        "L",
        "U",
    ]

    expected_meters_list = [
        461937,
        56407,
        356671,
        863240,
        367720,
        266681,
        577262,
        829975,
        112010,
        829975,
        491645,
        686074,
        5411,
        500254,
    ]
    assert all(
        instr.meters == expected_meters
        for instr, expected_meters in zip(dig_plan, expected_meters_list)
    )

    assert all(
        mapping[instr.direction] == expected_direction
        for instr, expected_direction in zip(dig_plan, expected_directions_list)
    )

    pick_area_including_exterior = compute_area(dig_plan)
    assert pick_area_including_exterior == 952408144115
