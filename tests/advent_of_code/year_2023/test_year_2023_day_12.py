import numpy as np
from advent_of_code.year_2023.year_2023_day_12 import (
    analyse_group,
    compute_possible_arrangements,
    parse_text_input,
    unfold_records,
)

EXAMPLE_INPUT = """

???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1

"""


def test_year_2023_day_12_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    history_list = []
    for record, group in parsed_input:
        print("-------------")
        history = set()
        _ = analyse_group(record, record, group, history)
        history_list.append(history)
    assert [len(h) for h in history_list] == [1, 4, 1, 1, 4, 10]
    assert sum([len(h) for h in history_list]) == 21
    ...


def test_year_2023_day_12_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    multiplied = [unfold_records(i, 5) for i in parsed_input]
    assert multiplied[0][0].tostring() == b"???.###????.###????.###????.###????.###"
    assert multiplied[0][1] == (1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3)

    multiple_multiplied = [
        [unfold_records(i, k) for i in parsed_input] for k in range(1, 6)
    ]
    multiple_multiplied_histories = [
        compute_possible_arrangements([unfold_records(i, k) for i in parsed_input])
        for k in range(1, 3)
    ]

    sequence = np.array(multiple_multiplied_histories)
    un_plus_one_on_un = (np.roll(sequence, -1, axis=0) // sequence)[:-1][0]

    assert np.all(
        un_plus_one_on_un
        == np.array([[1, 8, 1, 2, 5, 15], [1, 8, 1, 2, 5, 15], [1, 8, 1, 2, 5, 15]])
    )

    fifth_iteration = sequence[0] * (un_plus_one_on_un ** (5 - 1))
    u_n = sequence
    ratio = (u_n[1] ** 4) // (u_n[0] ** 3)

    expected_result = np.array([1, 16384, 1, 16, 2500, 506250])
    assert np.all(fifth_iteration == expected_result)
    assert np.all(ratio == expected_result)
    assert np.sum(fifth_iteration) == 525152


def test_year_2023_day_12_part_2_naive():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    multiplied = [unfold_records(i, 5) for i in parsed_input]
    assert multiplied[0][0].tostring() == b"???.###????.###????.###????.###????.###"
    assert multiplied[0][1] == (1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3)
    history_list = []
    for record, group in multiplied:
        print("-------------")
        history = set()
        _ = analyse_group(record, record, group, history)
        history_list.append(history)
    result = sum([len(h) for h in history_list])

    assert [len(h) for h in history_list] == [1, 16384, 1, 16, 2500, 506250]
    assert sum([len(h) for h in history_list]) == 525152
    # 16384 / 4 = 4096
    # 16 / 1 = 16
    # 2500 / 4 = 625
    # 506250 / 10 = 5062
    ...
