import numpy as np

from advent_of_code.year_2023.year_2023_day_12 import (
    analyse_group_v2,
    compute_possible_arrangements,
    count_arrangements,
    parse_text_input,
    parse_text_input_v2,
    unfold_records,
    unfold_records_v2,
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
        _ = analyse_group_v2(record, record, group, history)
        history_list.append(history)
    assert [len(h) for h in history_list] == [1, 4, 1, 1, 4, 10]
    assert sum([len(h) for h in history_list]) == 21
    ...


def test_year_2023_day_12_part_2_old():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    multiplied = [unfold_records(i, 5) for i in parsed_input]
    assert multiplied[0][0].tostring() == b"???.###????.###????.###????.###????.###"
    assert multiplied[0][1] == (1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3)

    multiple_multiplied_histories = [
        compute_possible_arrangements([unfold_records(i, k) for i in parsed_input])
        for k in range(1, 5)
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
        _ = analyse_group_v2(record, record, group, history)
        history_list.append(history)

    assert [len(h) for h in history_list] == [1, 16384, 1, 16, 2500, 506250]
    assert sum([len(h) for h in history_list]) == 525152
    # 16384 / 4 = 4096
    # 16 / 1 = 16
    # 2500 / 4 = 625
    # 506250 / 10 = 5062
    ...


# TODO memoize with tuples
# Simplify repeated sequences
# of hash and dot


def test_year_2023_day_12_part_2_second_try():
    # See https://www.reddit.com/r/adventofcode/
    # comments/18hbjdi/2023_day_12_part_2_this_image_helped_a_few_people/
    # No need for recursion at all... only a kind of "allowed states" mechanism
    # Verify that part 1 still works with the new solution on one line
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input_v2(test_input)
    example_line = parsed_input[-1]
    assert example_line == ("?###????????", (3, 2, 1))
    result = count_arrangements(*example_line)
    assert result == 10

    # Verify whole part 1
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input_v2(test_input)
    arrangement_counts = [
        count_arrangements(record, group) for (record, group) in parsed_input
    ]
    assert arrangement_counts == [1, 4, 1, 1, 4, 10]
    assert sum(arrangement_counts) == 21

    # Verify whole part 2
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input_v2(test_input)
    multiplied = [unfold_records_v2(i, 5) for i in parsed_input]
    assert multiplied[0][0] == "???.###????.###????.###????.###????.###"
    assert multiplied[0][1] == (1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3)
    arrangement_counts = [
        count_arrangements(record, group) for (record, group) in multiplied
    ]
    assert arrangement_counts == [1, 16384, 1, 16, 2500, 506250]
    assert sum(arrangement_counts) == 525152
