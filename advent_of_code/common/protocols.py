from abc import abstractmethod
from dataclasses import dataclass
from typing import Mapping, Protocol

from advent_of_code.common.common import load_puzzle_input_text_file


class AdventOfCodeProblem[PuzzleInputT](Protocol):
    """Base class for Advent of Code problems' implementations"""

    year: int  # This is a protocol member
    day: int
    tag: str = "v1"  # This one too (with default)

    @abstractmethod
    def solve_part_1(self, puzzle_input: PuzzleInputT) -> int | str:
        raise NotImplementedError

    @abstractmethod
    def solve_part_2(self, puzzle_input: PuzzleInputT) -> int | str:
        raise NotImplementedError

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInputT:
        raise NotImplementedError

    def parse_input_text_file(self) -> PuzzleInputT:
        text = load_puzzle_input_text_file(self.year, self.day)
        parsed = self.parse_text_input(text)
        return parsed

    def solve(
        self, part_1: bool = True, part_2: bool = True
    ) -> Mapping[int, int | str | None]:
        # Be safe and parse twice the input, in case logic require input mutation
        # This is less efficient than reusing the input, but can help keep independence
        # in part solving, when it is easier to mutate the puzzle input inplace.
        result_part_1 = (
            self.solve_part_1(self.parse_input_text_file()) if part_1 else None
        )
        result_part_2 = (
            self.solve_part_2(self.parse_input_text_file()) if part_2 else None
        )

        return {1: result_part_1, 2: result_part_2}


@dataclass(kw_only=True, frozen=True)
class ExampleAdventOfCodePuzzleInputYYYYDD1:
    number: int


@dataclass(kw_only=True, frozen=True)
class ExampleAdventOfCodePuzzleInputYYYYDD2:
    number_bis: int


@dataclass(kw_only=True, frozen=True)
class ExampleAdventOfCodeProblem202206(
    AdventOfCodeProblem[ExampleAdventOfCodePuzzleInputYYYYDD1]
):
    year: int
    day: int
    # Explicit subclassing will bring the tag attribute and its default value
    # But it can still be overridden
    tag: str = "retest"

    def solve_part_1(self, puzzle_input: ExampleAdventOfCodePuzzleInputYYYYDD1):
        return 1

    def solve_part_2(self, puzzle_input: ExampleAdventOfCodePuzzleInputYYYYDD1):
        return "hey"

    @staticmethod
    def parse_text_input(text: str) -> ExampleAdventOfCodePuzzleInputYYYYDD1:
        return ExampleAdventOfCodePuzzleInputYYYYDD1(number=int(text))

    #  Explicit subclassing = We get the parse_input_text_file default implementation for free


@dataclass(kw_only=True)
class ExampleAdventOfCodeProblem202207:
    year: int
    day: int
    tag: str = "v1"
    # Implicit subclassing requires setting the tag attribute manually

    def solve_part_1(self, puzzle_input: ExampleAdventOfCodePuzzleInputYYYYDD2) -> int:
        return 231

    def solve_part_2(self, puzzle_input: ExampleAdventOfCodePuzzleInputYYYYDD2) -> str:
        return "hop"

    @staticmethod
    def parse_text_input(text: str) -> ExampleAdventOfCodePuzzleInputYYYYDD2:
        return ExampleAdventOfCodePuzzleInputYYYYDD2(number_bis=int(text))

    # Implicit subclassing = We need to manually define this boilerplate method
    # Conclusion: if default implementation is needed, use explicit subclassing
    def parse_input_text_file(self) -> ExampleAdventOfCodePuzzleInputYYYYDD2:
        text = load_puzzle_input_text_file(self.year, self.day)
        parsed = self.parse_text_input(text)
        return parsed

    def solve(self, part_1: bool = True, part_2: bool = True):
        result_part_1 = self.solve_part_1(self.parse_input_text_file())
        result_part_2 = self.solve_part_2(self.parse_input_text_file())

        return {1: result_part_1, 2: result_part_2}


def function_that_solve_part_1[PuzzleInputT](
    problem: AdventOfCodeProblem[PuzzleInputT], puzzle_input: PuzzleInputT
) -> int | str:
    result = problem.solve_part_1(puzzle_input=puzzle_input)
    return result


if __name__ == "__main__":
    # Explicit subclassing. With Protocol as a dataclass itself, the tag attribute is inherited
    problem = ExampleAdventOfCodeProblem202206(year=2022, day=6)
    puzzle_input = ExampleAdventOfCodePuzzleInputYYYYDD1(number=34)

    res1 = function_that_solve_part_1(problem, puzzle_input)

    # Implicit subclassing. The tag cannot be passed directly, it must be declared
    problem = ExampleAdventOfCodeProblem202207(year=2022, day=7)
    puzzle_input = ExampleAdventOfCodePuzzleInputYYYYDD2(number_bis=343)

    res2 = function_that_solve_part_1(problem, puzzle_input)

    print(res1, res2)
