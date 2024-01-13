from advent_of_code.year_2023.year_2023_day_15 import (
    add_up_focusing_power,
    hash_year_2023_day_15,
    hash_year_2023_day_15_imperative,
    hashmap_process,
    parse_text_input,
    render_step,
)

EXAMPLE_INPUT = """

rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7

"""

EXPECTED_INITIALIZATION_SEQUENCE_PART_2 = """
After "rn=1":
Box 0: [rn 1]

After "cm-":
Box 0: [rn 1]

After "qp=3":
Box 0: [rn 1]
Box 1: [qp 3]

After "cm=2":
Box 0: [rn 1] [cm 2]
Box 1: [qp 3]

After "qp-":
Box 0: [rn 1] [cm 2]

After "pc=4":
Box 0: [rn 1] [cm 2]
Box 3: [pc 4]

After "ot=9":
Box 0: [rn 1] [cm 2]
Box 3: [pc 4] [ot 9]

After "ab=5":
Box 0: [rn 1] [cm 2]
Box 3: [pc 4] [ot 9] [ab 5]

After "pc-":
Box 0: [rn 1] [cm 2]
Box 3: [ot 9] [ab 5]

After "pc=6":
Box 0: [rn 1] [cm 2]
Box 3: [ot 9] [ab 5] [pc 6]

After "ot=7":
Box 0: [rn 1] [cm 2]
Box 3: [ot 7] [ab 5] [pc 6]
"""


def test_year_2023_day_15_simple_hash():
    assert hash_year_2023_day_15_imperative("HASH") == 52
    assert hash_year_2023_day_15("HASH") == 52


def test_year_2023_day_15_part_1():
    test_input = EXAMPLE_INPUT
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


def test_year_2023_day_15_part_2():
    test_input = EXAMPLE_INPUT
    init_sequence = parse_text_input(test_input)

    rendered_steps = []
    for i in range(1, len(init_sequence) + 1):
        first_steps = init_sequence[:i]
        boxes = hashmap_process(first_steps)
        rendered_steps.append(render_step(boxes, first_steps[-1]))

    rendered_steps_visu = "\n\n".join(rendered_steps)
    assert rendered_steps_visu == EXPECTED_INITIALIZATION_SEQUENCE_PART_2.strip()

    boxes = hashmap_process(init_sequence)
    assert add_up_focusing_power(boxes) == 145
    ...
