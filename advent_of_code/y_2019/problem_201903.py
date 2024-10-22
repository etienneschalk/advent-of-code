from dataclasses import dataclass

import numpy as np

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = list[list[tuple[str, int]]]


@dataclass(kw_only=True)
class AdventOfCodeProblem201903(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2019
    day: int = 3

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return [
            [(word[0], int(word[1:])) for word in line.split(",")]
            for line in text.strip().split("\n")
        ]

    def solve_part_1(self, puzzle_input: PuzzleInput):
        print(puzzle_input)
        # Step 1: Compute segments sets for two wires (get abs coords from rel movements)
        wire_coords = self.compute_coords_set(puzzle_input)

        # Step 2: Bruteforce cartesian product of two segment sets.
        centres, all_combined_steps = self.extreme_unhinged_bruteforce(wire_coords)

        print(centres)
        print(all_combined_steps)
        result_part_1 = min(sum(abs(p) for p in c) for c in centres)
        print(result_part_1)  # part 1

        # part 2
        result_part_2 = min(all_combined_steps)
        print(f"{result_part_2=}")
        return result_part_1

    def compute_coords_set(self, puzzle_input):
        wire_coords = []
        for wire_moves in puzzle_input:
            coords = [np.array((0, 0))]
            for move in wire_moves:
                direction, quantity = move
                if direction == "R":
                    new_coord = (coords[-1][0] + quantity, coords[-1][1])
                elif direction == "L":
                    new_coord = (coords[-1][0] - quantity, coords[-1][1])
                elif direction == "D":
                    new_coord = (coords[-1][0], coords[-1][1] - quantity)
                elif direction == "U":
                    new_coord = (coords[-1][0], coords[-1][1] + quantity)
                coords.append(np.array(new_coord))
            wire_coords.append(coords)

        print(wire_coords)
        return wire_coords

    def extreme_unhinged_bruteforce(self, wire_coords):
        centres = []
        all_combined_steps = []
        steps_0 = 0
        for start_0, end_0 in zip(wire_coords[0][:-1], wire_coords[0][1:]):
            vec_0 = end_0 - start_0
            steps_0 += abs(sum(vec_0))
            steps_1 = 0
            for start_1, end_1 in zip(wire_coords[1][:-1], wire_coords[1][1:]):
                vec_1 = end_1 - start_1
                steps_1 += abs(sum(vec_1))

                dot = np.dot(vec_0, vec_1)
                # bypass parallel segments
                # ignore case where two segments are superposed.
                if dot == 0:
                    i = int(vec_1[1] == 0)
                    # ignore edges (strict comparison only)
                    if (
                        min(start_1[1 - i], end_1[1 - i])
                        < start_0[1 - i]
                        < max(start_1[1 - i], end_1[1 - i])
                    ) and (
                        min(start_0[i], end_0[i])
                        < start_1[i]
                        < max(start_0[i], end_0[i])
                    ):
                        centre = start_1[i], start_0[1 - i]
                        if i == 1:  # y, x coords are reversed
                            centre = centre[1], centre[0]
                        centre = np.array(centre)
                        print(f"found {centre=} {steps_0=} {steps_1=}")
                        centres.append(centre)

                        # Remove excess steps with centre:
                        excess = sum(abs(end_0 - centre)) + sum(abs(end_1 - centre))
                        print("excess", excess)
                        print(end_0, centre, end_1)
                        combined_steps = steps_0 + steps_1 - excess
                        all_combined_steps.append(combined_steps)
        return centres, all_combined_steps

    def solve_part_2(self, puzzle_input: PuzzleInput):
        print(puzzle_input)
        # Step 1: Compute segments sets for two wires (get abs coords from rel movements)
        wire_coords = self.compute_coords_set(puzzle_input)

        # Step 2: Bruteforce cartesian product of two segment sets.
        centres, all_combined_steps = self.extreme_unhinged_bruteforce(wire_coords)

        # part 2
        result_part_2 = min(all_combined_steps)
        print(f"{result_part_2=}")
        return result_part_2


def run_program(program):
    pc = 0  # Program Counter
    while program[pc] != 99:
        if program[pc] == 1:
            program[program[pc + 3]] = (
                program[program[pc + 1]] + program[program[pc + 2]]
            )
            pc += 4
        elif program[pc] == 2:
            program[program[pc + 3]] = (
                program[program[pc + 1]] * program[program[pc + 2]]
            )
            pc += 4


if __name__ == "__main__":
    print(AdventOfCodeProblem201903().solve())
