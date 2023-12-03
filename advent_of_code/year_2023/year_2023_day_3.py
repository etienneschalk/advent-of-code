from pathlib import Path

import numpy as np
import numpy.typing as npt

DataType = npt.NDArray[np.char_]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    # games = load_input_text_file()

    answer = None
    return answer


def compute_part_2():
    # games = load_input_text_file()

    answer = None
    return answer


def load_input_text_file() -> DataType:
    input_path = "resources/advent_of_code/year_2023/input_year_2023_day_2.txt"
    input_path = Path(input_path)
    assert input_path.is_file()
    text = input_path.read_text()
    games = parse_text_input(text)
    assert len(games) == 100
    return games


def parse_text_input(text: str) -> DataType:
    game_str_list = text.strip().split("\n")
    return game_str_list


if __name__ == "__main__":
    main()
