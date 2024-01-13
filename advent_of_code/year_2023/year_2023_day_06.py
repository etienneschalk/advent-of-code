import operator
from functools import reduce  # Valid in Python 2.6+, required in Python 3

import numpy as np

from advent_of_code.common import load_input_text_file_from_filename


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    data = parse_input_text_file()
    number_of_ways = compute_number_of_ways_to_win(data)
    return number_of_ways


def compute_part_2():
    data = parse_input_text_file()
    data = correct_data(data)
    number_of_ways = compute_number_of_ways_to_win(data)
    return number_of_ways


def parse_input_text_file() -> ...:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ...:
    lines = text.strip().split("\n")
    time_line = lines[0].split()
    distance_line = lines[1].split()
    return {
        time_line[0]: [int(i) for i in time_line[1:]],
        distance_line[0]: [int(i) for i in distance_line[1:]],
    }


def correct_data(races: dict[str, list[int]]) -> dict[str, list[int]]:
    return {
        key: [int("".join(str(i) for i in races[key]))]
        for key in ("Time:", "Distance:")
    }


def compute_number_of_ways_to_win(parsed_input):
    results = compute_ranges(parsed_input)
    number_of_ways = reduce(operator.mul, (t[1] - t[0] + 1 for t in results), 1)
    return number_of_ways


def compute_ranges(races: dict[str, list[int]]) -> list[tuple[int, int]]:
    results = []
    for time, record_distance in zip(races["Time:"], races["Distance:"]):
        T = time
        k = record_distance
        # solutions = [
        #     (T / 2) * (1 + sign * np.sqrt(1 - (4 * k) / T**2)) for sign in (-1, 1)
        # ]
        solutions = [(T + sign * np.sqrt(T**2 - 4 * k)) / 2 for sign in (-1, 1)]
        # Add epsilon to force "strictly superior"
        solutions[0] = int(np.ceil(solutions[0] + np.finfo(np.float32).eps))
        solutions[1] = int(np.floor(solutions[1] - np.finfo(np.float32).eps))
        results.append(solutions)
    return results


if __name__ == "__main__":
    main()
