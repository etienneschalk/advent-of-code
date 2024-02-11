from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2023.year_2023_day_15 import (
    add_up_focusing_power,
    hash_year_2023_day_15,
    hash_year_2023_day_15_imperative,
    hashmap_process,
    parse_text_input,
    render_step,
)


def test_year_2023_day_15_simple_hash():
    assert hash_year_2023_day_15_imperative("HASH") == 52
    assert hash_year_2023_day_15("HASH") == 52


def test_year_2023_day_15_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    actual_result = {i: hash_year_2023_day_15(i) for i in parsed_input}
    expected_result = {
        "rn=1": 30,
        "cm-": 253,
        "qp=3": 97,
        "cm=2": 47,
        "qp-": 14,
        "pc=4": 180,
        "ot=9": 9,
        "ab=5": 197,
        "pc-": 48,
        "pc=6": 214,
        "ot=7": 231,
    }
    assert actual_result == expected_result
    assert sum(expected_result.values()) == 1320


def test_year_2023_day_15_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    init_sequence = parse_text_input(test_input)

    rendered_steps = []
    for i in range(1, len(init_sequence) + 1):
        first_steps = init_sequence[:i]
        boxes = hashmap_process(first_steps)
        rendered_steps.append(render_step(boxes, first_steps[-1]))

    rendered_steps_visu = "\n\n".join(rendered_steps)
    expected = example_inputs.retrieve(
        __file__, "EXPECTED_INITIALIZATION_SEQUENCE_PART_2"
    )
    assert rendered_steps_visu == expected.strip()

    boxes = hashmap_process(init_sequence)
    assert add_up_focusing_power(boxes) == 145
    ...
