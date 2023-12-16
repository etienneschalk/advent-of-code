import numpy as np

from advent_of_code.year_2023.year_2023_day_12 import analyse_group, parse_text_input

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
    ...
