import numpy as np

from advent_of_code.common import load_input_text_file

ProblemDataType = ...


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    parsed_input = parse_input_text_file()
    history_list = []
    for record, group in parsed_input:
        print("-------------")
        history = set()
        _ = analyse_group(record, record, group, history)
        history_list.append(history)
    result = sum([len(h) for h in history_list])
    return result


def compute_part_2():
    data = parse_input_text_file()
    ...
    return None


def analyse_group(
    full_record: np.ndarray,
    record: np.ndarray,
    group: tuple[int],
    history: set[str],
    damaged_count: int = 0,
) -> int:
    # print(f"{len(record):02d}", record, group, damaged_count)
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


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    parsed = []
    for line in lines:
        record, group = line.split(" ")
        group = tuple(int(c) for c in group.split(","))
        parsed.append((np.fromstring(record, dtype="<S1"), group))
    return parsed


if __name__ == "__main__":
    main()
