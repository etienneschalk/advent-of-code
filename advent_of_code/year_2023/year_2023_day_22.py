from dataclasses import dataclass
import numpy as np
from advent_of_code.common import load_input_text_file


@dataclass(kw_only=True)
class Brick:
    position: tuple[np.ndarray, np.ndarray]
    falling: bool
    shadow: np.ndarray | None = None

    @property
    def rank(self) -> int:
        return min(coord[2] for coord in self.position)

    @property
    def lowest_z(self) -> int:
        return min(coord[2] for coord in self.position)

    @property
    def highest(self) -> int:
        return max(coord[2] for coord in self.position)


ProblemDataType = list[Brick]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    data = parse_input_text_file()
    ...
    return None


def compute_part_2():
    data = parse_input_text_file()
    ...
    return None


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")

    bricks = [
        Brick(
            position=tuple(
                np.fromstring(part, dtype=int, sep=",") for part in line.split("~")
            ),
            falling=True,
        )
        for line in lines
    ]
    # 1,1,8~1,1,9

    return bricks


if __name__ == "__main__":
    main()
