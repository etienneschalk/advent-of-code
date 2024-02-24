from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

from advent_of_code.common.common import (
    get_example_inputs_file_contents,
    get_expected_answers_file_contents,
)
from advent_of_code.common.protocols import AdventOfCodeProblem


@dataclass(frozen=True, kw_only=True)
class ExampleInputsStore:
    _store: dict[str, Any]

    def retrieve(self, test_file_path: str, content_id: str = "EXAMPLE_INPUT") -> str:
        test_file_path = Path(test_file_path).stem

        content = self._store[test_file_path][content_id]
        content = str(content)  # should only contain str, not anything else.
        return content

    @classmethod
    def from_private_resources_repository(cls, year: int) -> Self:
        parsed_toml = get_example_inputs_file_contents(year)
        return cls(_store=parsed_toml)


@dataclass(frozen=True, kw_only=True)
class ExpectedAnswersStore:
    _store: dict[str, Any]

    def retrieve(self, aoc_problem: AdventOfCodeProblem[Any]) -> dict[int, str | int]:
        identifier = f"{aoc_problem.year}{aoc_problem.day:02d}"

        content = self._store[identifier]
        content = {int(k): v for k, v in content.items()}
        return content

    @classmethod
    def from_private_resources_repository(cls, year: int) -> Self:
        parsed_json = get_expected_answers_file_contents(year)
        return cls(_store=parsed_json)
