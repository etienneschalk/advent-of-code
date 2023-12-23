from collections import defaultdict
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
        return min(self.z0, self.z1)

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
    def length(self) -> int:
        # The bricks span in only one direction
        # So all deltas will be null except for the brick's direction
        # Hence it is safe to sum to eliminate the null values
        return np.sum(self.pos1 - self.pos0)

    @property
    def height(self) -> int:
        # +1 because the position tuple is inclusive
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
        else:  # pos0 and pos1 are equal = 1m3
            indexer = tuple(self.pos0)

        return indexer

    @property
    def is_position_ordered(self) -> bool:
        return np.all(self.pos1 >= self.pos0)


ProblemDataType = list[Brick]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    data = parse_input_text_file()
    result = compute_safely_removable_bricks(data)
    return result
    # {1: 471, 2: None}
    # That's not the right answer; your answer is too high.
    # Curiously, it's the right answer for someone else; you might be logged in
    # to the wrong account or just unlucky. In any case,
    # you need to be using your puzzle input. If you're stuck, make sure you're
    # using the full input data; there are also some general tips on the about page,
    # or you can ask for hints on the subreddit.
    # Please wait one minute before trying again. [Return to Day 22]


def compute_part_2():
    data = parse_input_text_file()
    ...
    return None


def compute_safely_removable_bricks(unsorted_bricks: list[Brick]) -> int:
    # Bricks that are the closest to the ground have the most priority (low-leaning z)
    sorted_bricks = sorted(unsorted_bricks, key=lambda b: b.rank)

    # The input is well-formed, no need to max min min max, positions are ordered.
    assert np.all([sorted_brick.is_position_ordered for sorted_brick in sorted_bricks])

    elevation_map = create_elevation_map(sorted_bricks)
    fallen_bricks = compute_fallen_bricks(sorted_bricks, elevation_map)

    space = create_space_datacuboid(fallen_bricks)
    fill_space_with_bricks_identifiers(fallen_bricks, space)

    supported_bricks = compute_supported_bricks(fallen_bricks, space)
    support_counts = compute_support_counts(supported_bricks)
    support_counts = dict(support_counts)
    can_be_disintegrated = compute_disintegrable_bricks(
        supported_bricks, support_counts
    )
    safely_removable_bricks = sum(can_be_disintegrated.values())

    return safely_removable_bricks


def compute_disintegrable_bricks(
    supported_bricks: dict[int, tuple[int, ...]],
    support_counts: dict[int, int],
) -> dict[int, bool]:
    # For the record: put an any instead of a all.
    # Was producing the wrong output.
    # Changed it to all, then it worked...
    # When coding and inverting boolean logic on collections,
    # ALWAYS double-check the quantifier!!!!
    return {
        brick_id: all(support_counts[sb_id] > 1 for sb_id in supported_bricks_ids)
        or not supported_bricks_ids
        for brick_id, supported_bricks_ids in supported_bricks.items()
    }


def compute_supported_bricks(
    fallen_bricks: list[Brick], space: np.ndarray
) -> dict[int, tuple[int, ...]]:
    actual_supported: dict[int, tuple[int, ...]] = {}
    for fallen_brick in fallen_bricks:
        xx, yy, zz = fallen_brick.indexer
        if isinstance(zz, slice):
            new_zz = zz.stop
        else:  # zz is an int
            new_zz = zz + 1
        just_above_indexer = (xx, yy, new_zz)
        just_above = space[just_above_indexer]
        supported = tuple(np.unique(just_above[just_above > 0]))
        actual_supported[fallen_brick.identifier] = supported
    return actual_supported


def compute_support_counts(
    supported_bricks: dict[int, tuple[int, ...]]
) -> dict[int, int]:
    # Unsafe when support_count == 1 (it means one support only)
    # Note: bricks supported by the ground are not in the support counts
    support_counts = defaultdict(int)
    for brick_id, supported_bricks_ids in supported_bricks.items():
        for supported_brick_id in supported_bricks_ids:
            support_counts[supported_brick_id] += 1
    return support_counts


def fill_space_with_bricks_identifiers(
    fallen_bricks: list[Brick], space: np.ndarray
) -> None:
    for fallen_brick in fallen_bricks:
        space[fallen_brick.indexer] = fallen_brick.identifier


def create_space_datacuboid(fallen_bricks: list[Brick]) -> np.ndarray:
    xmax = max(max(b.x0, b.x1) for b in fallen_bricks)
    ymax = max(max(b.y0, b.y1) for b in fallen_bricks)
    zmax = max(max(b.z0, b.z1) for b in fallen_bricks)
    # space_shape = (xmax + 1, ymax + 1, zmax + 1)
    space_shape = (xmax + 1, ymax + 1, zmax + 2)
    space = np.zeros(space_shape, dtype=int)
    return space


def compute_fallen_bricks(
    sorted_bricks: list[Brick], elevation_map: np.ndarray
) -> list[Brick]:
    fallen_bricks = []
    for idx, brick in enumerate(sorted_bricks, 1):
        # elevation_map = (x,y)-2D array containing max(z)
        # use elevation_map to know if the brick can still fall
        # only use the x and y parts of the indexer for the elevation_map
        fallen_brick = create_fallen_brick(elevation_map, idx, brick)
        fallen_bricks.append(fallen_brick)

    return fallen_bricks


def create_fallen_brick(
    elevation_map: np.ndarray, identifier: int, brick: Brick
) -> Brick:
    indexer = brick.indexer[:2]
    peak = np.max(elevation_map[indexer])
    new_peak = peak + brick.height
    elevation_map[indexer] = new_peak
    dz = brick.z1 - new_peak
    dpos = np.array((0, 0, dz))
    fallen_position = (brick.pos0 - dpos, brick.pos1 - dpos)
    fallen_brick = Brick(
        position=fallen_position,
        falling=False,
        identifier=identifier,
    )

    return fallen_brick


def create_elevation_map(sorted_bricks: list[Brick]) -> np.ndarray:
    xmax = max(max(b.x0, b.x1) for b in sorted_bricks)
    ymax = max(max(b.y0, b.y1) for b in sorted_bricks)
    elevation_map_shape = (xmax + 1, ymax + 1)
    elevation_map = np.zeros(elevation_map_shape, dtype=int)

    return elevation_map


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
