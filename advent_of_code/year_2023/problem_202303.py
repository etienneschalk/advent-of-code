from collections import defaultdict
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from advent_of_code.common.common import parse_2d_string_array_to_uint8
from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = npt.NDArray[np.uint8]


@dataclass(kw_only=True)
class AdventOfCodeProblem202303(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 3

    def solve_part_1(self, puzzle_input: PuzzleInput):
        assert len(puzzle_input) == 140 + 2  # + 2 comes from padding

        flattened = find_part_numbers(puzzle_input)
        answer = sum(flattened)
        return answer

    def solve_part_2(self, puzzle_input: PuzzleInput):
        gear_part_numbers_tuples = find_part_numbers_and_gears(puzzle_input)
        gear_ratios = [t[0] * t[1] for t in gear_part_numbers_tuples]
        sum_of_gear_ratios = sum(gear_ratios)
        answer = sum_of_gear_ratios
        return answer

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)


def parse_text_input(text: str) -> PuzzleInput:
    input_array = parse_2d_string_array_to_uint8(text)

    # Add a border of dots will ease later checks,
    # not having to care about data outside the borders
    padded_array = np.pad(input_array, pad_width=1, constant_values=ord(b"."))

    return padded_array


# Part 1
def find_part_numbers(array: PuzzleInput) -> list[int]:
    adjacent_numbers_for_row = [
        [t[0] for t in detect_adjacent_numbers_in_line(array, row_index)]
        for row_index in range(array.shape[0])
    ]
    flattened = [j for i in adjacent_numbers_for_row for j in i]
    return flattened


# Part 2
def find_part_numbers_and_gears(array: PuzzleInput) -> list[tuple[int, ...]]:
    adjacent_numbers_for_row = [
        detect_adjacent_numbers_in_line(array, row_index)
        for row_index in range(array.shape[0])
    ]
    flattened = [j for i in adjacent_numbers_for_row for j in i]
    graph: dict[tuple[int, ...] | None, list[int]] = defaultdict(list)
    for pair in flattened:
        part_number = pair[0]
        # There at most one gear (empirically constated previously)
        candidate_gear = next(iter(pair[1])) if pair[1] else None
        graph[candidate_gear].append(part_number)
    gear_part_numbers_tuples = [
        tuple(value) for value in graph.values() if len(value) == 2
    ]
    return gear_part_numbers_tuples


def detect_adjacent_numbers_in_line(array: PuzzleInput, row_index: int):
    line = array[row_index]
    digit_was_detected = False
    adjacent_numbers: list[tuple[int, set[tuple[int, ...]]]] = []
    stack_values: list[int] = []
    col_start = -1  # fix the unbound issue
    for i in range(line.shape[0]):
        digit_is_detected = chr(line[i]).isdigit()
        if digit_is_detected:
            if not digit_was_detected:
                digit_was_detected = True
                col_start = i
            stack_values.append(line[i])
        else:
            if digit_was_detected:
                digit_was_detected = False
                # only the first stack_indices is useful actually
                if not is_solitary_number(array, row_index, col_start, i):
                    number = int("".join(chr(i) for i in stack_values))
                    candidate_gear_coordinates_list = (
                        get_candidate_gear_coordinates_list(
                            array, row_index, col_start, i
                        )
                    )
                    adjacent_numbers.append((number, candidate_gear_coordinates_list))

                stack_values.clear()
    return adjacent_numbers


def is_solitary_number(
    array: PuzzleInput, row_index: int, col_start_inclusive: int, col_end_exclusive: int
) -> bool:
    # A number is considered solitary (non-adjacent) if it is circled by dots.
    return all(
        array[coords] == ord(b".")
        for coords in get_neighbouring_coordinates_tuple(
            row_index, col_start_inclusive, col_end_exclusive
        )
    )


def get_candidate_gear_coordinates_list(
    array: PuzzleInput, row_index: int, col_start_inclusive: int, col_end_exclusive: int
) -> set[tuple[int, int]]:
    target_char = ord(b"*")
    neighbouring_coordinates_generator = get_neighbouring_coordinates_tuple(
        row_index, col_start_inclusive, col_end_exclusive
    )
    candidate_gear_coordinates_set = {
        neighbouring_coordinates
        for neighbouring_coordinates in neighbouring_coordinates_generator
        if array[neighbouring_coordinates] == target_char
    }

    # Good to know: a part number is connected to at most one candidate gear.
    assert len(candidate_gear_coordinates_set) <= 1

    return candidate_gear_coordinates_set


def get_neighbouring_coordinates_tuple(
    row_index: int, col_start_inclusive: int, col_end_exclusive: int
) -> tuple[tuple[int, int], ...]:
    return (
        (row_index, col_start_inclusive - 1),  # left
        (row_index, col_end_exclusive),  # right
        # upper row
        *(
            (row_index - 1, col)
            for col in range(col_start_inclusive - 1, col_end_exclusive + 1)
        ),
        # lower row
        *(
            (row_index + 1, col)
            for col in range(col_start_inclusive - 1, col_end_exclusive + 1)
        ),
    )


if __name__ == "__main__":
    print(AdventOfCodeProblem202303().solve())
