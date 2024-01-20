import operator
from dataclasses import dataclass
from functools import reduce

import numpy as np

from advent_of_code.protocols import AdventOfCodeProblem

type PuzzleInput = dict[str, list[int]]


@dataclass(kw_only=True)
class AdventOfCodeProblem202306(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 6

    def solve_part_1(self, puzzle_input: PuzzleInput):
        return compute_number_of_ways_to_win(puzzle_input)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        data = correct_data(puzzle_input)
        number_of_ways = compute_number_of_ways_to_win(data)
        return number_of_ways

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)


def parse_text_input(text: str) -> PuzzleInput:
    lines = text.strip().split("\n")
    time_line = lines[0].split()
    distance_line = lines[1].split()
    parsed = {
        time_line[0]: [int(i) for i in time_line[1:]],
        distance_line[0]: [int(i) for i in distance_line[1:]],
    }
    return parsed


def correct_data(races: PuzzleInput) -> PuzzleInput:
    return {
        key: [int("".join(str(i) for i in races[key]))]
        for key in ("Time:", "Distance:")
    }


def compute_number_of_ways_to_win(parsed_input: PuzzleInput):
    results = compute_ranges(parsed_input)
    number_of_ways = reduce(operator.mul, (t[1] - t[0] + 1 for t in results), 1)
    return number_of_ways


def compute_ranges(races: PuzzleInput) -> list[tuple[int, int]]:
    return [
        compute_range(time, record_distance)
        for time, record_distance in zip(races["Time:"], races["Distance:"])
    ]


def compute_range(time: int, record_distance: int):
    T = time
    k = record_distance
    solutions = tuple((T + sign * np.sqrt(T**2 - 4 * k)) / 2 for sign in (-1, 1))
    # Add epsilon to force "strictly superior"
    solutions = (
        int(np.ceil(solutions[0] + np.finfo(np.float32).eps)),
        int(np.floor(solutions[1] - np.finfo(np.float32).eps)),
    )

    return solutions


if __name__ == "__main__":
    print(AdventOfCodeProblem202306().solve())
