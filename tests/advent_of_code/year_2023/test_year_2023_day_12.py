import numpy as np

from advent_of_code.year_2023.year_2023_day_12 import parse_text_input

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
    ...


def analyse_group(
    full_record: np.ndarray,
    record: np.ndarray,
    group: tuple[int],
    history: set[str],
    damaged_count: int = 0,
) -> int:
    print(f"{len(record):02d}", record, group, damaged_count)
    if len(group) == 0:
        if np.all(record != b"#"):
            print("Found")
            history.add(full_record.tostring())
            return 1
        else:
            return 0
    if record.size == 0:
        if len(group) == 1 and damaged_count == group[0]:
            print("Found")
            history.add(full_record.tostring())
            return 1
        else:
            return 0
    if record[0] == b"#":
        damaged_count += 1
        if damaged_count > group[0]:
            return 0
        else:
            return analyse_group(full_record, record[1:], group, history, damaged_count)
    elif record[0] == b".":
        if damaged_count != 0:
            # we just exited a group
            if damaged_count == group[0]:
                # we counted the expected amount of #
                group = group[1:]
                damaged_count = 0
                return analyse_group(
                    full_record, record[1:], group, history, damaged_count
                )
            else:
                # failure: not enough
                return 0
        else:
            # we are just browsing dots
            damaged_count = 0
            return analyse_group(full_record, record[1:], group, history, damaged_count)
    else:
        found = 0
        record[0] = b"#"
        found += analyse_group(full_record, record, group, history, damaged_count)
        record[0] = b"."
        found += analyse_group(full_record, record, group, history, damaged_count)
        record[0] = b"?"

        return found


def test_year_2023_day_12_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    ...
