from advent_of_code.year_2023.year_2023_day_12 import (
    count_arrangements,
    parse_text_input_v2,
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


def test_year_2023_day_12_part_1_second_try():
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


def test_year_2023_day_12_part_2_second_try():
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
