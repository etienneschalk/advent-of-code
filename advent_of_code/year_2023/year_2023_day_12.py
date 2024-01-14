from dataclasses import dataclass

from advent_of_code.protocols import AdventOfCodeProblem

type PuzzleLine = tuple[str, tuple[int, ...]]
type PuzzleInput = list[PuzzleLine]

# [visu] No easy visualisation rn, as recursion is rapidly reduced for performance (sum, no history)


@dataclass(kw_only=True)
class AdventOfCodeProblem202312(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 12

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input_v2(text)

    def solve_part(self, puzzle_input: PuzzleInput, iter_count: int):
        multiplied = [unfold_records_v2(i, iter_count) for i in puzzle_input]
        arrangement_counts = [
            count_arrangements(record, group) for (record, group) in multiplied
        ]
        result = sum(arrangement_counts)
        return result

    def solve_part_1(self, puzzle_input: PuzzleInput):
        return self.solve_part(puzzle_input, iter_count=1)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        return self.solve_part(puzzle_input, iter_count=5)


@dataclass(frozen=True)
class StateKey:
    group: int
    amount: int


def count_arrangements(springs: str, groups: tuple[int, ...]) -> int:
    # Completely taken from
    # https://www.reddit.com/r/adventofcode/comments/18hbjdi/2023_day_12_part_2_this_image_helped_a_few_people/
    permutations = 1
    states: dict[StateKey, int] = {StateKey(group=0, amount=0): permutations}
    damaged_left = springs.count("#") + springs.count("?")
    minimal_required_damaged_left = [sum(groups[i:]) for i in range(len(groups))]
    next_states: dict[StateKey, int] = {}
    for spring in springs:
        if spring != ".":
            damaged_left -= 1
        for state, permutations in states.items():
            group, amount = state.group, state.amount
            if spring == "#" or spring == "?":
                if group < len(groups) and amount < groups[group]:
                    key = StateKey(group, amount + 1)
                    next_states[key] = permutations
            if spring == "." or spring == "?":
                if amount == 0:
                    key = StateKey(group, 0)
                    next_states[key] = permutations + next_states.get(key, 0)
                elif amount == groups[group]:
                    key = StateKey(group + 1, 0)
                    next_states[key] = permutations + next_states.get(key, 0)

        # Keep only possible states
        next_states = {
            k: v
            for k, v in next_states.items()
            if k.group == len(groups)
            or damaged_left + k.amount >= minimal_required_damaged_left[k.group]
        }

        states.clear()
        states, next_states = next_states, states
    return sum(states.values())


def parse_text_input_v2(text: str) -> PuzzleInput:
    lines = text.strip().split("\n")
    parsed: list[tuple[str, tuple[int, ...]]] = []
    for line in lines:
        record, group = line.split(" ")
        group = tuple(int(c) for c in group.split(","))
        parsed.append((record, group))
    return parsed


def unfold_records_v2(input_line: PuzzleLine, iter_count: int = 5):
    record, group = input_line
    return (
        "?".join(record for _ in range(iter_count)),
        group * iter_count,
    )


if __name__ == "__main__":
    print(AdventOfCodeProblem202312().solve_all())
