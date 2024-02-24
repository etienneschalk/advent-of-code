from dataclasses import dataclass
from itertools import combinations

import numpy as np
import numpy.typing as npt
import sympy as sym

from advent_of_code.common.common import load_input_text_file_from_filename
from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = list[Hailstone]


@dataclass(kw_only=True)
class AdventOfCodeProblem202324(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 24

    def solve_part_1(self, puzzle_input: PuzzleInput):
        hailstones = puzzle_input

        xmin = ymin = 200000000000000
        xmax = ymax = 400000000000000

        logs = []
        qualified = []

        solve_part_1(hailstones, qualified, xmin, ymin, xmax, ymax, logs=logs)

        result = len(qualified)

        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        hailstones = puzzle_input
        # Only 4 hailstones are needed...
        offset = 0
        result = solve_part_2(hailstones[offset : 4 + offset])
        return result

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)


@dataclass(frozen=True, kw_only=True)
class Hailstone:
    position: npt.NDArray[np.int32]
    velocity: npt.NDArray[np.int32]

    def __str__(self):
        p_str = ", ".join(str(i) for i in self.position)
        v_str = ", ".join(str(i) for i in self.velocity)
        return f"{p_str} @ {v_str}"

    @classmethod
    def from_string(cls, string: str) -> "Hailstone":
        position, velocity = [
            [int(c) for c in el.split(", ")] for el in string.split(" @ ")
        ]
        return cls(position=np.array(position), velocity=np.array(velocity))

    @property
    def px(self) -> int:
        return self.position[0]

    @property
    def py(self) -> int:
        return self.position[1]

    @property
    def pz(self) -> int:
        return self.position[2]

    @property
    def vx(self) -> int:
        return self.velocity[0]

    @property
    def vy(self) -> int:
        return self.velocity[1]

    @property
    def vz(self) -> int:
        return self.velocity[2]


def solve_part_1(
    hailstones: list[Hailstone],
    qualified: list[tuple[Hailstone, Hailstone]],
    xmin: int,
    ymin: int,
    xmax: int,
    ymax: int,
    *,
    logs: list[str] | None = None,
):
    for pair in combinations(hailstones, 2):
        ha, hb = pair

        if logs is not None:
            logs.append(f"Hailstone A: {ha}")
            logs.append(f"Hailstone B: {hb}")

        cross_product_velocities = np.cross(ha.velocity, hb.velocity)
        parallel_trajectories = np.all(cross_product_velocities == 0)

        if parallel_trajectories:
            if logs is not None:
                message = "Hailstones' paths are parallel; they never intersect."
                logs.append(message)

        else:
            # First express y = f(x)
            m1, b1 = get_affine_coefficients(ha)
            m2, b2 = get_affine_coefficients(hb)

            x_sol = (b2 - b1) / (m1 - m2)
            y_sol = m1 * x_sol + b1

            # Intersection de droites mais pas de segments
            # Check the demi-droite
            future_ha = check_intersection_in_future(ha, x_sol)
            future_hb = check_intersection_in_future(hb, x_sol)

            inside = (xmin <= x_sol <= xmax) and (ymin <= y_sol <= ymax)

            if (future_ha and future_hb) and inside:
                qualified.append(pair)

            if logs is not None:
                location_str = "inside" if inside else "outside"
                f_x_sol = int(x_sol) if x_sol % 1 == 0 else round(x_sol, 3)
                f_y_sol = int(y_sol) if y_sol % 1 == 0 else round(y_sol, 3)
                details = f"(at x={f_x_sol}, y={f_y_sol})"

                if future_ha and future_hb:
                    message = (
                        f"Hailstones' paths will cross {location_str} "
                        f"the test area {details}."
                    )
                elif not future_ha and future_hb:
                    message = "Hailstones' paths crossed in the past for hailstone A."
                elif future_ha and not future_hb:
                    message = "Hailstones' paths crossed in the past for hailstone B."
                else:
                    message = (
                        "Hailstones' paths crossed in the past for both hailstones."
                    )

                logs.append(message)

        if logs is not None:
            logs.append("")

    return logs


def solve_part_2(
    hailstones: list[Hailstone],
) -> int:
    """
    CHEATING

    Source largely taken from:
    https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/keqorhn/

    The sum of the coordinates of the initial position
    """

    # All vector positions are aligned at their own time when crossing the thrown hailstone.
    # The equation solver solves this
    # h_i = p_i + t_i b_i
    p = [[h.px, h.py, h.pz] for h in hailstones]
    v = [[h.vx, h.vy, h.vz] for h in hailstones]

    t0, t1, t2, t3, l1, l2 = sym.symbols("t0, t1, t2, t3, l1, l2")

    eqs = [
        # (p_2(t_2) - p_0(t_0)) = lambda_1 (p_1(t_1) - p_0(t_0))
        *[
            sym.Eq(
                (p[2][i] - p[0][i]) + t2 * v[2][i] - t0 * v[0][i],
                l1 * ((p[1][i] - p[0][i]) + t1 * v[1][i] - t0 * v[0][i]),
            )
            for i in range(3)
        ],
        # (p_3(t_3) - p_0(t_0)) = lambda_1 (p_1(t_1) - p_0(t_0))
        *[
            sym.Eq(
                (p[3][i] - p[0][i]) + t3 * v[3][i] - t0 * v[0][i],
                l2 * ((p[1][i] - p[0][i]) + t1 * v[1][i] - t0 * v[0][i]),
            )
            for i in range(3)
        ],
    ]

    solution = sym.solve(eqs, [t0, t1, t2, t3, l1, l2])
    s = solution[0]

    # s[0] = t0, s[1] = t1
    rocks = [
        [
            (s[j] * (p[0][i] + s[0] * v[0][i]) - s[0] * (p[j][i] + s[j] * v[j][i]))
            / (s[j] - s[0])
            for i in range(3)
        ]
        for j in range(1, 4)
    ]

    # Any t1 or t2 or t1 can be used with t0
    sum_rocks = [sum(rock) for rock in rocks]

    assert sum_rocks[0] == sum_rocks[1]
    assert sum_rocks[0] == sum_rocks[2]

    return sum_rocks[0]


def check_intersection_in_future(hailstone: Hailstone, x_sol: float):
    return (
        (hailstone.vx > 0 and x_sol > hailstone.px)
        or hailstone.vx < 0
        and x_sol < hailstone.px
    )


def get_affine_coefficients(hailstone: Hailstone) -> tuple[float, float]:
    m1 = hailstone.vy / hailstone.vx
    b1 = hailstone.py - m1 * hailstone.px
    return m1, b1


def parse_input_text_file() -> PuzzleInput:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> PuzzleInput:
    lines = text.strip().split("\n")
    hailstones = [Hailstone.from_string(line) for line in lines]
    return hailstones


if __name__ == "__main__":
    print(AdventOfCodeProblem202324().solve())
