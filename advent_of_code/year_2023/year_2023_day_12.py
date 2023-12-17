from dataclasses import dataclass
from fractions import Fraction

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
        history = set()
        _ = analyse_group_v2(record, record, group, history)
        history_list.append(history)
    result = sum([len(h) for h in history_list])
    return result


def compute_part_2():
    text = load_input_text_file(__file__)
    parsed_input = parse_text_input_v2(text)
    multiplied = [unfold_records_v2(i, 5) for i in parsed_input]
    arrangement_counts = [
        count_arrangements(record, group) for (record, group) in multiplied
    ]
    result = sum(arrangement_counts)
    return result


def compute_part_2_old():
    parsed_input = parse_input_text_file()[:16]
    iter_count = 5
    iter_count_to_compute = 4
    u_n = np.array(
        [
            compute_possible_arrangements([unfold_records(i, k) for i in parsed_input])
            for k in range(1, iter_count_to_compute)
        ]
    )
    # u_n_plus_one_on_u_n = (np.roll(u_n, -1, axis=0) // u_n)[:-1][0]

    # possible_arrangements = u_n[0] * (u_n_plus_one_on_u_n ** (iter_count - 1))

    # Some are slow but does not correspond to those whose ratio changes:
    # 5: ?.???????.????. 5,1,1
    # 7: ??.???????????.? 4,2
    # array([[ 1,  3, 37,  3,  6, 43,  7, 51, 12,  1,  9,  7,  3,  5,  3,  3],
    #        [ 1,  3, 37,  3,  6, 44,  7, 58, 12,  1,  9,  7,  3,  5,  3,  3]])
    # or...
    # with_errors = (u_n[1] ** 4) / (u_n[0] ** 4)
    ratio = (u_n[1] ** 4) // (u_n[0] ** 3)
    ratio = (u_n[1] ** 4) // (u_n[0] ** 3)
    ratio = (u_n[1] ** (iter_count - 1)) // (u_n[0] ** (iter_count - 2))
    [Fraction(x, y) for x, y in zip(u_n[1], u_n[0])]
    # Non-integer denominators must be calculated manually?
    len(
        [
            f
            for f in [Fraction(x, y) for x, y in zip(u_n[1], u_n[0])]
            if f.denominator != 1
        ]
    )
    91464976098328  # too low
    5223100092137  # too low
    result = sum(ratio)
    return result


def compute_possible_arrangements(multiplied):
    history_list = []
    history = set()
    for idx, line in enumerate(multiplied):
        record, group = line
        print("-------------", idx)
        _ = analyse_group_v2(record, record, group, history)
        history_list.append(len(history))
        history.clear()
    return history_list


# def num_valid_solutions(record: str, groups: tuple[int, ...]) -> int:


# TODO Simplify this logic, put tuples, use a cache, simplify repeated sequence
# Find sum, do not try to compute the history, it's too much
# Only two parameters: record being a string or tuple, and groups tuple.
def analyse_group_v2(
    full_record: np.ndarray,
    record: np.ndarray,
    group: tuple[int, ...],
    history: set[str],
    damaged_count: int = 0,
) -> int:
    # print(f"{len(record):02d}", record, group, damaged_count)
    if len(group) == 0:
        if np.all(record != b"#"):
            # print("Found")
            history.add(full_record.tostring())
            return 1
        else:
            return 0
    if record.size == 0:
        if len(group) == 1 and damaged_count == group[0]:
            # print("Found")
            history.add(full_record.tostring())
            return 1
        else:
            return 0
    if record[0] == b"#":
        damaged_count += 1
        if damaged_count > group[0]:
            return 0
        else:
            return analyse_group_v2(
                full_record, record[1:], group, history, damaged_count
            )
    elif record[0] == b".":
        if damaged_count != 0:
            # we just exited a group
            if damaged_count == group[0]:
                # we counted the expected amount of #
                group = group[1:]
                damaged_count = 0
                return analyse_group_v2(
                    full_record, record[1:], group, history, damaged_count
                )
            else:
                # failure: not enough
                return 0
        else:
            # we are just browsing dots
            damaged_count = 0
            return analyse_group_v2(
                full_record, record[1:], group, history, damaged_count
            )
    else:
        found = 0
        record[0] = b"#"
        found += analyse_group_v2(full_record, record, group, history, damaged_count)
        record[0] = b"."
        found += analyse_group_v2(full_record, record, group, history, damaged_count)
        record[0] = b"?"

        return found


def unfold_records(input_line, iter_count: int = 5):
    record, group = input_line
    return (
        np.tile(np.pad(record, (0, 1), constant_values="?"), iter_count)[:-1],
        group * iter_count,
    )


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


@dataclass(frozen=True)
class StateKey:
    group: int
    amount: int


def count_arrangements(springs: str, groups: tuple[int, ...]) -> int:
    # Completely taken from
    # https://www.reddit.com/r/adventofcode/comments/18hbjdi/2023_day_12_part_2_this_image_helped_a_few_people/
    permutations = 1
    states: dict[StateKey, int] = {StateKey(group=0, amount=0): permutations}
    damaged_left = springs.count("#") + springs.count("?")
    minimal_required_damaged_left = [sum(groups[i:]) for i in range(len(groups))]
    next_states: dict[StateKey, int] = {}
    for spring in springs:
        if spring != ".":
            damaged_left -= 1
        for state, permutations in states.items():
            group, amount = state.group, state.amount
            if spring == "#" or spring == "?":
                if group < len(groups) and amount < groups[group]:
                    key = StateKey(group, amount + 1)
                    next_states[key] = permutations
            if spring == "." or spring == "?":
                if amount == 0:
                    key = StateKey(group, 0)
                    next_states[key] = permutations + next_states.get(key, 0)
                elif amount == groups[group]:
                    key = StateKey(group + 1, 0)
                    next_states[key] = permutations + next_states.get(key, 0)

        # Keep only possible states
        next_states = {
            k: v
            for k, v in next_states.items()
            if k.group == len(groups)
            or damaged_left + k.amount >= minimal_required_damaged_left[k.group]
        }

        states.clear()
        states, next_states = next_states, states
    return sum(states.values())


def parse_text_input_v2(text: str) -> list[tuple[str, tuple[int, ...]]]:
    lines = text.strip().split("\n")
    parsed = []
    for line in lines:
        record, group = line.split(" ")
        group = tuple(int(c) for c in group.split(","))
        parsed.append((record, group))
    return parsed


def unfold_records_v2(input_line, iter_count: int = 5):
    record, group = input_line
    return (
        "?".join(record for i in range(iter_count)),
        group * iter_count,
    )


if __name__ == "__main__":
    main()
