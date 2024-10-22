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

        # Step 2: Bruteforce cartesian product of two segment sets.
        centres = []
        for start_0, end_0 in zip(wire_coords[0][:-1], wire_coords[0][1:]):
            for start_1, end_1 in zip(wire_coords[1][:-1], wire_coords[1][1:]):
                vec_0 = end_0 - start_0
                vec_1 = end_1 - start_1
                dot = np.dot(vec_0, vec_1)
                # bypass parallel segments
                # ignore case where two segments are superposed.
                if dot == 0:
                    if vec_1[0] == 0:
                        start_h, end_h = start_0, end_0
                        start_v, end_v = start_1, end_1
                    else:
                        start_v, end_v = start_0, end_0
                        start_h, end_h = start_1, end_1

                    hmin = min(start_h[0], end_h[0])
                    hmax = max(start_h[0], end_h[0])
                    hy = start_h[1]

                    vmin = min(start_v[1], end_v[1])
                    vmax = max(start_v[1], end_v[1])
                    vx = start_v[0]

                    # ignore edges (strict comparison only)
                    if (vmin < hy < vmax) and (hmin < vx < hmax):
                        centre = vx, hy
                        print(f"found centre {centre=}")
                        centres.append(centre)
        print(centres)
        result = min(sum(abs(p) for p in c) for c in centres)
        print(result)
        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        return -1


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
