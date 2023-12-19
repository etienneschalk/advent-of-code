from dataclasses import asdict, dataclass
from typing import Literal

from advent_of_code.common import load_input_text_file

ProblemDataType = ...


@dataclass(frozen=True, kw_only=True)
class PartRating:
    x: int
    m: int
    a: int
    s: int

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(frozen=True, kw_only=True)
class Rule:
    category: str
    operator: Literal["<", ">"]
    rating: int
    destination_workflow: str

    def apply(self, part: PartRating) -> bool:
        if self.operator == "<":
            return part[self.category] < self.rating
        else:
            return part[self.category] > self.rating


@dataclass(frozen=True, kw_only=True)
class Workflow:
    name: str
    rules: tuple[Rule]
    destination_workflow_else: str

    def apply(self, part: PartRating) -> str:
        for rule in self.rules:
            if rule.apply(part):
                return rule.destination_workflow
        return self.destination_workflow_else


@dataclass(frozen=True, kw_only=True)
class PuzzleInput:
    workflows: dict[str, Workflow]
    part_ratings: list[PartRating]

    def apply(self, part: PartRating) -> str:
        final_destinations = {"A", "R"}
        dest = "in"
        while dest not in final_destinations:
            dest = self.workflows[dest].apply(part)
        return dest

    def apply_to_all(self) -> list[str]:
        return [self.apply(part) for part in self.part_ratings]

    def solve_part_1(self) -> int:
        return {
            idx: sum(asdict(part).values())
            for idx, part in enumerate(self.part_ratings)
            if self.apply(part) == "A"
        }


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    parsed_input = parse_input_text_file()
    solve_1 = parsed_input.solve_part_1()
    return sum(solve_1.values())


def compute_part_2():
    data = parse_input_text_file()
    ...
    return None


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    blocks = text.strip().split("\n\n")
    workflows_raw = blocks[0].split("\n")
    part_ratings_raw = blocks[1].split("\n")
    workflows = [parse_workflow(line) for line in workflows_raw]
    part_ratings = [
        PartRating(
            **dict(
                (el.split("=")[0], int(el.split("=")[1]))
                for el in line[1:-1].split(",")
            )
        )
        for line in part_ratings_raw
    ]
    return PuzzleInput(
        workflows={w.name: w for w in workflows}, part_ratings=part_ratings
    )


def parse_workflow(wf: str) -> Workflow:
    split = wf.split("{")
    name = split[0]
    rules_raw = split[1][:-1].split(",")
    rules = tuple(parse_rule(r) for r in rules_raw[:-1])
    destination_workflow_else = rules_raw[-1]
    return Workflow(
        name=name, rules=rules, destination_workflow_else=destination_workflow_else
    )


def parse_rule(ru: str) -> Rule:
    rest, dest = ru.split(":")
    op_idx = max(rest.find(">"), rest.find("<"))
    return Rule(
        category=rest[:op_idx],
        operator=rest[op_idx],
        rating=int(rest[op_idx + 1 :]),
        destination_workflow=dest,
    )


if __name__ == "__main__":
    main()
