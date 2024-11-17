from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = int


@dataclass(kw_only=True)
class AdventOfCodeProblem201916(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2019
    day: int = 16

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return [int(word) for word in text.strip().split("\n")][0]

    def solve_part_1(self, puzzle_input: PuzzleInput):
        return solve_part_1_func(puzzle_input, 100)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        pass


def obtain_pattern(
    input_signal_length: int, position: int
) -> npt.NDArray[np.integer[Any]]:
    base_pattern = np.array([0, 1, 0, -1])
    repeated = np.repeat(base_pattern, position + 1)
    tile_repeats: int = input_signal_length // base_pattern.size + 2
    tiled = np.tile(repeated, tile_repeats)[1:][:input_signal_length]
    return tiled


def compute_phase(
    input_signal_arr: npt.NDArray[np.integer[Any]],
    patterns_arr: npt.NDArray[np.integer[Any]],
) -> npt.NDArray[np.integer[Any]]:
    input_signal_tiled_arr = np.tile(input_signal_arr, (input_signal_arr.size, 1))
    print(input_signal_tiled_arr)

    product = input_signal_tiled_arr * patterns_arr
    print(product)

    next_input_signal_arr = np.abs(product.sum(axis=1)) % 10
    print(next_input_signal_arr)
    return next_input_signal_arr


def convert_integer_to_array_of_its_digits(
    input_signal: str,
) -> npt.NDArray[np.integer[Any]]:
    return np.array([int(digit) for digit in input_signal])


def test_example_input_simple():
    input_signal = 12345678
    input_signal_arr = convert_integer_to_array_of_its_digits(str(input_signal))

    patterns = [
        obtain_pattern(input_signal_arr.size, i).tolist()
        for i in range(input_signal_arr.size)
    ]
    print(patterns)

    assert patterns == [
        [1, 0, -1, 0, 1, 0, -1, 0],
        [0, 1, 1, 0, 0, -1, -1, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1],
    ]

    patterns_arr = np.array(patterns)
    print(patterns_arr)

    expected_signals = ["48226158", "34040438", "03415518", "01029498"]
    for expected_signal in expected_signals:
        input_signal_arr = compute_phase(input_signal_arr, patterns_arr)
        print(input_signal_arr)
        assert (
            input_signal_arr == convert_integer_to_array_of_its_digits(expected_signal)
        ).all()

    powers_of_ten = 10 ** np.arange(0, input_signal_arr.size)[::-1]
    print(powers_of_ten)

    result = str(np.dot(powers_of_ten, input_signal_arr)).zfill(input_signal_arr.size)
    print(result)


def test_example_input_larger(
    input_signal: int,
    expected_first_eight_digits_of_the_final_output_list_after_100_phases: str,
    phase_count: int = 100,
):
    result = solve_part_1_func(input_signal, phase_count)

    assert (
        result == expected_first_eight_digits_of_the_final_output_list_after_100_phases
    )
    print(result)


def solve_part_1_func(input_signal: int, phase_count: int):
    input_signal_arr = convert_integer_to_array_of_its_digits(str(input_signal))

    patterns = [
        obtain_pattern(input_signal_arr.size, i).tolist()
        for i in range(input_signal_arr.size)
    ]
    patterns_arr = np.array(patterns)

    for _ in range(phase_count):
        input_signal_arr = compute_phase(input_signal_arr, patterns_arr)

    input_signal_arr = input_signal_arr[:8]  # Keep only 8 first digits
    powers_of_ten = 10 ** np.arange(0, input_signal_arr.size)[::-1]
    result = str(np.dot(powers_of_ten, input_signal_arr)).zfill(input_signal_arr.size)
    return result


if __name__ == "__main__":
    test_example_input_simple()
    test_example_input_larger(80871224585914546619083218645595, "24176176")
    test_example_input_larger(19617804207202209144916044189917, "73745418")
    test_example_input_larger(69317163492948606335995924319873, "52432133")
    print(AdventOfCodeProblem201916().solve())
