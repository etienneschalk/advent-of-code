from collections import defaultdict
from dataclasses import dataclass

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = list[tuple[str, str]]


@dataclass(kw_only=True)
class AdventOfCodeProblem201906(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2019
    day: int = 6

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        parsed = [
            orbital_relationship.split(")")
            for orbital_relationship in text.strip().split("\n")
        ]
        return [(c[0], c[1]) for c in parsed]

    def solve_part_1(self, puzzle_input: PuzzleInput):
        orbit_map = create_orbit_map_parent_to_children(puzzle_input)
        root = "COM"
        total = explore(orbit_map, root)
        return total

    def solve_part_2(self, puzzle_input: PuzzleInput):
        # Use trees property
        orbit_map = create_orbit_map_child_to_parent(puzzle_input)
        print(orbit_map)

        parent = "YOU"
        lineage_you = [parent]
        while True:
            parent = orbit_map[parent]
            lineage_you.append(parent)
            if parent == "COM":
                break
        lineage_you = lineage_you[::-1]
        print(lineage_you, len(lineage_you))

        parent = "SAN"
        lineage_san = [parent]
        while True:
            parent = orbit_map[parent]
            lineage_san.append(parent)
            if parent == "COM":
                break
        lineage_san = lineage_san[::-1]
        print(lineage_san, len(lineage_san))

        # Find common ancestor for both YOU and SAN
        print(lineage_you[:30])
        print(lineage_san[:30])

        common_ancestor_idx = common_ancestor = -1
        for i in range(min(len(lineage_you), len(lineage_san))):
            if lineage_you[i] == lineage_san[i]:
                print("same")
                common_ancestor_idx, common_ancestor = i, lineage_you[i]
            else:
                print(common_ancestor_idx, common_ancestor)
                print(lineage_you[common_ancestor_idx:])
                print(lineage_san[common_ancestor_idx:])
                # Add the lengths of the two chains
                total = (len(lineage_you[common_ancestor_idx:]) - 2) + (
                    (len(lineage_san[common_ancestor_idx:])) - 2
                )
                return total
        raise RuntimeError


def create_orbit_map_parent_to_children(puzzle_input):
    # Parent to children
    orbit_map: dict[str, list[str]] = defaultdict(list)
    for parent, child in puzzle_input:
        orbit_map[parent].append(child)
    return orbit_map


def create_orbit_map_child_to_parent(puzzle_input):
    # Child to parent (each child has a unique parent)
    orbit_map: dict[str, str] = {}
    for parent, child in puzzle_input:
        orbit_map[child] = parent
    return orbit_map


def explore(orbit_map, node_name, depth: int = 0):
    total = depth
    if node_name in orbit_map:
        for child in orbit_map[node_name]:
            total += explore(orbit_map, child, depth + 1)
    return total


if __name__ == "__main__":
    print(AdventOfCodeProblem201906().solve())
