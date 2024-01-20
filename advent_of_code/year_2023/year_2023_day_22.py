from collections import defaultdict
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from advent_of_code.protocols import AdventOfCodeProblem

type SupportCounts = dict[int, int]
type PuzzleInput = list[Brick]

# [visu] Would look good with a 3d engine showing the bricks fall, with GUI controls


@dataclass(kw_only=True)
class AdventOfCodeProblem202322(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 22

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        result = compute_safely_removable_bricks_count(puzzle_input)
        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        supported_bricks = compute_supported_bricks_from_initial_bricks(puzzle_input)
        support_counts = compute_support_counts(supported_bricks)

        # 81610 too high
        # 55713 That's not the right answer; your answer is too low.
        result = solve_part_2(supported_bricks, support_counts, True)

        return result


@dataclass(kw_only=True)
class Brick:
    position: tuple[npt.NDArray[np.int64], npt.NDArray[np.int64]]
    falling: bool
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
    def pos0(self) -> npt.NDArray[np.int64]:
        return self.position[0]

    @property
    def pos1(self) -> npt.NDArray[np.int64]:
        return self.position[1]

    @property
    def length(self) -> np.int64:
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
    def is_position_ordered(self) -> np.bool_:
        return np.all(self.pos1 >= self.pos0)


def solve_part_2(
    supported_bricks: dict[int, tuple[int, ...]],
    support_counts: SupportCounts,
    dangerous_only: bool = False,
):
    can_be_disintegrated = compute_disintegrable_bricks(
        supported_bricks, support_counts
    )

    updated_support_counts_when_node_removed = (
        compute_updated_support_counts_when_node_removed(
            supported_bricks, support_counts
        )
    )

    if dangerous_only:
        dangerous_bricks = {
            k: v
            for k, v in updated_support_counts_when_node_removed.items()
            if not can_be_disintegrated[k]
        }
    else:
        dangerous_bricks = updated_support_counts_when_node_removed

    dangerous_consequences = compute_chain_reaction_other_fallen_bricks_count(
        dangerous_bricks
    )
    other_bricks_that_would_fall_count = sum(dangerous_consequences.values())
    return other_bricks_that_would_fall_count


def compute_updated_support_counts_when_node_removed(
    supported_bricks: dict[int, tuple[int, ...]],
    support_counts: SupportCounts,
):
    updated_support_counts_when_node_removed: dict[int, SupportCounts] = {}
    for b_id in supported_bricks.keys():
        sc = dict(support_counts)  # copy support counts, it will be mutated

        q = [b_id]
        while q:
            node = q.pop(0)
            for child in supported_bricks[node]:
                sc[child] -= 1
                if sc[child] == 0:
                    q.append(child)

        updated_support_counts_when_node_removed[b_id] = sc
    return updated_support_counts_when_node_removed


def compute_chain_reaction_other_fallen_bricks_count(
    updated_support_counts_when_node_removed: dict[int, SupportCounts],
):
    return {
        node: sum(v == 0 for v in value.values())
        for node, value in updated_support_counts_when_node_removed.items()
    }


def compute_safely_removable_bricks_count(unsorted_bricks: list[Brick]) -> int:
    supported_bricks = compute_supported_bricks_from_initial_bricks(unsorted_bricks)
    support_counts = compute_support_counts(supported_bricks)
    can_be_disintegrated = compute_disintegrable_bricks(
        supported_bricks, support_counts
    )
    safely_removable_bricks = sum(can_be_disintegrated.values())

    return safely_removable_bricks


def compute_supported_bricks_from_initial_bricks(
    unsorted_bricks: list[Brick],
) -> dict[int, tuple[int, ...]]:
    # Bricks that are the closest to the ground have the most priority (low-leaning z)
    sorted_bricks = sorted(unsorted_bricks, key=lambda b: b.rank)

    # The input is well-formed, no need to max min min max, positions are ordered.
    assert np.all([sorted_brick.is_position_ordered for sorted_brick in sorted_bricks])

    elevation_map = create_elevation_map(sorted_bricks)
    fallen_bricks = compute_fallen_bricks(sorted_bricks, elevation_map)

    space = create_space_datacuboid(fallen_bricks)
    fill_space_with_bricks_identifiers(fallen_bricks, space)

    supported_bricks = compute_supported_bricks(fallen_bricks, space)
    return supported_bricks


def compute_disintegrable_bricks(
    supported_bricks: dict[int, tuple[int, ...]],
    support_counts: SupportCounts,
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
    fallen_bricks: list[Brick], space: npt.NDArray[np.int64]
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
    supported_bricks: dict[int, tuple[int, ...]],
) -> SupportCounts:
    # Unsafe when support_count == 1 (it means one support only)
    # Note: bricks supported by the ground are not in the support counts
    support_counts = defaultdict(int)
    for _, supported_bricks_ids in supported_bricks.items():
        for supported_brick_id in supported_bricks_ids:
            support_counts[supported_brick_id] += 1
    return support_counts


def fill_space_with_bricks_identifiers(
    fallen_bricks: list[Brick], space: npt.NDArray[np.int64]
) -> None:
    for fallen_brick in fallen_bricks:
        space[fallen_brick.indexer] = fallen_brick.identifier


def create_space_datacuboid(fallen_bricks: list[Brick]) -> npt.NDArray[np.int64]:
    xmax = max(max(b.x0, b.x1) for b in fallen_bricks)
    ymax = max(max(b.y0, b.y1) for b in fallen_bricks)
    zmax = max(max(b.z0, b.z1) for b in fallen_bricks)
    # space_shape = (xmax + 1, ymax + 1, zmax + 1)
    space_shape = (xmax + 1, ymax + 1, zmax + 2)
    space = np.zeros(space_shape, dtype=int)
    return space


def compute_fallen_bricks(
    sorted_bricks: list[Brick], elevation_map: npt.NDArray[np.int64]
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
    elevation_map: npt.NDArray[np.int64], identifier: int, brick: Brick
) -> Brick:
    indexer = brick.indexer[:2]
    peak = np.max(elevation_map[indexer])
    new_peak = int(peak) + brick.height
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


def create_elevation_map(sorted_bricks: list[Brick]) -> npt.NDArray[np.int64]:
    xmax = max(max(b.x0, b.x1) for b in sorted_bricks)
    ymax = max(max(b.y0, b.y1) for b in sorted_bricks)
    elevation_map_shape = (xmax + 1, ymax + 1)
    elevation_map = np.zeros(elevation_map_shape, dtype=int)

    return elevation_map


def parse_text_input(text: str) -> PuzzleInput:
    lines = text.strip().split("\n")

    bricks = [parse_brick(line) for line in lines]
    # 1,1,8~1,1,9

    return bricks


def parse_brick(line: str):
    pos0, pos1 = (np.fromstring(part, dtype=int, sep=",") for part in line.split("~"))
    return Brick(
        position=(pos0, pos1),
        falling=True,
    )


if __name__ == "__main__":
    print(AdventOfCodeProblem202322().solve())
