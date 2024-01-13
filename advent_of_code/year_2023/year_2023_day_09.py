from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from advent_of_code.protocols import AdventOfCodeProblem

type PuzzleInput = npt.NDArray[np.int32]


@dataclass(kw_only=True)
class AdventOfCodeProblem202309(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 9

    def solve_part_1(self, puzzle_input: PuzzleInput):
        predictions = [predict_next_value_forward(arr) for arr in puzzle_input]
        return sum(predictions)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        predictions = [predict_next_value_backward(arr) for arr in puzzle_input]
        return sum(predictions)

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        lines = text.strip().split("\n")
        arrays = (np.fromstring(line, dtype=int, sep=" ") for line in lines)
        stacked = np.stack(list(arrays))
        return stacked


def predict_next_value_forward(arr: PuzzleInput) -> int:
    if np.all(arr == 0):
        return 0

    diff = compute_finite_difference_forward(arr)
    next_value = predict_next_value_forward(diff)
    result = arr[-1] + next_value
    return result


def predict_next_value_backward(arr: PuzzleInput) -> int:
    if np.all(arr == 0):
        return 0

    diff = compute_finite_difference_forward(arr)
    next_value = predict_next_value_backward(diff)
    result = arr[0] - next_value
    return result


def compute_finite_difference_forward(arr: PuzzleInput) -> PuzzleInput:
    return (np.roll(arr, -1) - arr)[:-1]


if __name__ == "__main__":
    print(AdventOfCodeProblem202309().solve_all())
