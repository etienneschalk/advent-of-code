from collections import defaultdict
from dataclasses import asdict, dataclass, replace
from typing import Any

import numpy as np

from advent_of_code.common.common import load_input_text_file_from_filename, save_txt
from advent_of_code.common.protocols import AdventOfCodeProblem

# [visu] Sankey flow diagram is the best suited

type PuzzleInput = PuzzleInputData


@dataclass(kw_only=True)
class AdventOfCodeProblem202319(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 19

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        solve_1 = puzzle_input.solve_part_1()
        return sum(solve_1.values())

    def solve_part_2(self, puzzle_input: PuzzleInput):
        initial_part_rating_range = construct_initial_part_range()
        solve_2 = puzzle_input.solve_part_2(initial_part_rating_range)
        return solve_2


@dataclass(frozen=True, kw_only=True)
class PartRating:
    x: int
    m: int
    a: int
    s: int

    def __getitem__(self, item: Any):
        return getattr(self, item)


@dataclass(frozen=True, kw_only=True)
class PartRatingRange:
    x: range
    m: range
    a: range
    s: range

    def __getitem__(self, item: Any):
        return getattr(self, item)

    def volume(self) -> int:
        volume = np.prod([r.stop - r.start for r in asdict(self).values()])
        return int(volume)


@dataclass(frozen=True, kw_only=True)
class PartRatingRangeTree:
    mapping: dict[str, list[PartRatingRange]]
    children: dict[str, list["PartRatingRangeTree"]] | None

    def __getitem__(self, item: Any):
        return getattr(self, item)


@dataclass(frozen=True, kw_only=True)
class Rule:
    category: str
    operator: str  # Literal["<", ">"]
    rating: int
    destination_workflow: str

    def apply(self, part: PartRating) -> bool:
        if self.operator == "<":
            return part[self.category] < self.rating
        else:
            return part[self.category] > self.rating

    def apply_to_range(
        self, part_range: PartRatingRange
    ) -> tuple[PartRatingRange, PartRatingRange]:
        min_inclusive = 1
        max_inclusive = 4000
        r = part_range[self.category]

        if self.operator == "<":
            lrange = intersect_ranges(r, range(min_inclusive, self.rating))
            rrange = intersect_ranges(r, range(self.rating, max_inclusive + 1))
            lpr = replace(part_range, **{self.category: lrange})
            rpr = replace(part_range, **{self.category: rrange})
            acc, rej = lpr, rpr
        else:  # == ">"
            lrange = intersect_ranges(r, range(min_inclusive, self.rating + 1))
            rrange = intersect_ranges(r, range(self.rating + 1, max_inclusive + 1))
            lpr = replace(part_range, **{self.category: lrange})
            rpr = replace(part_range, **{self.category: rrange})
            acc, rej = rpr, lpr
        return acc, rej


@dataclass(frozen=True, kw_only=True)
class Workflow:
    name: str
    rules: tuple[Rule, ...]
    destination_workflow_else: str

    def apply(self, part: PartRating) -> str:
        for rule in self.rules:
            if rule.apply(part):
                return rule.destination_workflow
        return self.destination_workflow_else

    def apply_to_range(
        self, part_range: PartRatingRange
    ) -> dict[str, list[PartRatingRange]]:
        # Beware of not overwriting keys in dicts!! Same issue as in day 05!
        # A destination can be split in multiple sub-ranges!!!!!
        accu = defaultdict(list)
        rej = part_range
        for rule in self.rules:
            acc, rej = rule.apply_to_range(rej)
            accu[rule.destination_workflow].append(acc)
        accu[self.destination_workflow_else].append(rej)
        return accu


@dataclass(frozen=True, kw_only=True)
class PuzzleInputData:
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

    def solve_part_1(self) -> dict[int, int]:
        return {
            idx: sum(asdict(part).values())
            for idx, part in enumerate(self.part_ratings)
            if self.apply(part) == "A"
        }

    def apply_to_range(
        self, initial_part_range: PartRatingRange, initial_dest: str = "in"
    ) -> PartRatingRangeTree | None:
        final_destinations = {"A", "R"}
        if initial_dest in final_destinations:
            return None

        mapping = self.workflows[initial_dest].apply_to_range(initial_part_range)

        children = {
            destination: [
                self.apply_to_range(part_range, destination)
                for part_range in part_ranges
            ]
            for destination, part_ranges in mapping.items()
        }
        children = {k: [el for el in v if el is not None] for k, v in children.items()}
        children = children if len(children) >= 1 else None
        recur_mapping = PartRatingRangeTree(mapping=mapping, children=children)
        return recur_mapping

    def solve_part_2(self, initial_part_range: PartRatingRange) -> int:
        applied = self.apply_to_range(initial_part_range)
        acc: list[list[PartRatingRange]] = []
        rej: list[list[PartRatingRange]] = []
        if applied is not None:
            gather_accepted_and_rejected_ranges(applied, acc, rej)
        result = sum([el.volume() for a in acc for el in a])
        return result


def gather_accepted_and_rejected_ranges(
    tree: PartRatingRangeTree,
    acc: list[list[PartRatingRange]],
    rej: list[list[PartRatingRange]],
):
    mapping, children = tree.mapping, tree.children

    acc_ranges = mapping.get("A")
    if acc_ranges is not None:
        acc.append(acc_ranges)

    rej_ranges = mapping.get("R")
    if rej_ranges is not None:
        rej.append(rej_ranges)

    if children is not None:
        for child in children.values():
            for el in child:
                gather_accepted_and_rejected_ranges(el, acc, rej)


def construct_initial_part_range(
    *, min_inclusive: int = 1, max_inclusive: int = 4000
) -> PartRatingRange:
    initial_range = range(min_inclusive, max_inclusive + 1)
    initial_part_rating_range = PartRatingRange(
        x=initial_range, m=initial_range, a=initial_range, s=initial_range
    )

    return initial_part_rating_range


def intersect_ranges(a: range, b: range) -> range:
    return range(max(a.start, b.start), min(a.stop, b.stop))


def parse_input_text_file() -> PuzzleInputData:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> PuzzleInputData:
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
    return PuzzleInputData(
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


def visu_recur_dict_part_2(mapping: PartRatingRangeTree, suffix: str = ""):
    import json

    txt = json.dumps(asdict(mapping), indent=4, default=str)

    save_txt(
        txt,
        f"part2{suffix}.json",
        __file__,
        output_subdir="text",
    )


if __name__ == "__main__":
    print(AdventOfCodeProblem202319().solve())
