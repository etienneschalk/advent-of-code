from dataclasses import dataclass

from advent_of_code.protocols import AdventOfCodeProblem

type PuzzleInput = tuple[tuple[str, str], ...]


@dataclass(kw_only=True)
class AdventOfCodeProblem202202(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2022
    day: int = 2

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        scores = compute_scores_for_part_1(puzzle_input)
        result = sum(scores)
        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        scores = compute_scores_for_part_2(puzzle_input)
        result = sum(scores)
        return result


def compute_scores_for_part_1(parsed_input: PuzzleInput):
    opponent_mapping = dict(zip("ABC", range(len("ABC"))))
    my_mapping = dict(zip("XYZ", range(len("XYZ"))))
    int_pairs = tuple((opponent_mapping[p[0]], my_mapping[p[1]]) for p in parsed_input)
    scores = compute_scores(int_pairs)
    return scores


def compute_scores_for_part_2(parsed_input: PuzzleInput):
    opponent_mapping = dict(zip("ABC", range(len("ABC"))))
    my_mapping = dict(zip("XYZ", (-1, 0, 1)))
    int_pairs = tuple(
        (opponent_mapping[p[0]], (opponent_mapping[p[0]] + my_mapping[p[1]]) % 3)
        for p in parsed_input
    )
    scores = compute_scores(int_pairs)
    return scores


def compute_scores(int_pairs: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    scores = tuple(3 * ((p[1] - p[0] + 1) % 3) + p[1] + 1 for p in int_pairs)
    return scores


def parse_text_input(text: str) -> PuzzleInput:
    return tuple(
        (line.split()[0], line.split()[1]) for line in text.strip().split("\n")
    )


if __name__ == "__main__":
    print(AdventOfCodeProblem202202().solve_all())
