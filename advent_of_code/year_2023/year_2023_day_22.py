from dataclasses import dataclass

import numpy as np

from advent_of_code.common import load_input_text_file


@dataclass(kw_only=True)
class Brick:
    position: tuple[np.ndarray, np.ndarray]
    falling: bool
    shadow: np.ndarray | None = None
    identifier: int = -1

    @property
    def rank(self) -> int:
        return min(coord[2] for coord in self.position)

    @property
    def lowest_z(self) -> int:
        return min(coord[2] for coord in self.position)

    @property
    def highest(self) -> int:
        return max(coord[2] for coord in self.position)

    @property
    def x0(self) -> int:
        return self.position[0][0]

    @property
    def x1(self) -> int:
        return self.position[1][0]

    @property
    def y0(self) -> int:
        return self.position[0][1]

    @property
    def y1(self) -> int:
        return self.position[1][1]

    @property
    def z0(self) -> int:
        return self.position[0][2]

    @property
    def z1(self) -> int:
        return self.position[1][2]

    @property
    def pos0(self) -> int:
        return self.position[0]

    @property
    def pos1(self) -> int:
        return self.position[1]

    @property
    def pos1(self) -> int:
        return self.position[1]

    @property
    def length(self) -> int:
        # The bricks span in only one direction
        # So all deltas will be null except for the brick's direction
        # Hence it is safe to sum to eliminate the null values
        return np.sum(self.pos1 - self.pos0)

    @property
    def height(self) -> int:
        # +1 because the position tuple is incluseive
        return self.z1 - self.z0 + 1

    @property
    def indexer(self) -> tuple[int | slice, ...]:
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        dz = self.z1 - self.z0

        # z-span brick (vertical)
        if dz != 0:
            min_z = self.z0
            indexer = (self.x0, self.y0, slice(min_z, min_z + dz + 1))
        # y-span brick (horizontal)
        elif dy != 0:
            min_y = self.y0
            indexer = (self.x0, slice(min_y, min_y + dy + 1), self.z0)
        # x-span brick (horizontal)
        elif dx != 0:
            min_x = self.x0
            indexer = (slice(min_x, min_x + dx + 1), self.y0, self.z0)
        else:
            raise ValueError("Incorrect Brick")

        return indexer


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
