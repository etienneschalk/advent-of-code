import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Mapping

import numpy as np
import numpy.typing as npt
import pygame

from advent_of_code.common import parse_2d_string_array_to_uint8
from advent_of_code.year_2023.year_2023_day_16 import (
    CELL_EMPTY_SPACE,
    CELL_MIRROR_BACKSLASH,
    CELL_MIRROR_SLASH,
    CELL_SPLITTER_H,
    CELL_SPLITTER_V,
    CELL_WALL,
    AdventOfCodeProblem202316,
)

type HistoryLine = tuple[int, tuple[int, int], tuple[int, int]]
type History = tuple[HistoryLine, ...]
type HistoryDictPerDepth = Mapping[int, list[HistoryLine]]

PATTERN_EMPTY_SPACE_3X3 = """
...
...
...
"""
PATTERN_MIRROR_SLASH_3X3 = """
..O
.O.
O..
"""
PATTERN_MIRROR_BACKSLASH_3X3 = """
O..
.O.
..O
"""
PATTERN_SPLITTER_V_3X3 = """
.O.
.O.
.O.
"""
PATTERN_SPLITTER_H_3X3 = """
...
OOO
...
"""
PATTERN_WALL_3X3 = """
OOO
OOO
OOO
"""
CELL_CHAR_TO_PATTERN_3X3_STRINGS = {
    CELL_EMPTY_SPACE: PATTERN_EMPTY_SPACE_3X3,
    CELL_MIRROR_SLASH: PATTERN_MIRROR_SLASH_3X3,
    CELL_MIRROR_BACKSLASH: PATTERN_MIRROR_BACKSLASH_3X3,
    CELL_SPLITTER_V: PATTERN_SPLITTER_V_3X3,
    CELL_SPLITTER_H: PATTERN_SPLITTER_H_3X3,
    CELL_WALL: PATTERN_WALL_3X3,
}

PATTERN_EMPTY_SPACE_5X5 = """
.....
.....
.....
.....
.....
"""
PATTERN_MIRROR_SLASH_5X5 = """
....O
...O.
..O..
.O...
O....
"""
PATTERN_MIRROR_BACKSLASH_5X5 = """
O....
.O...
..O..
...O.
....O
"""
PATTERN_SPLITTER_V_5X5 = """
..O..
..O..
..O..
..O..
..O..
"""
PATTERN_SPLITTER_H_5X5 = """
.....
.....
OOOOO
.....
.....
"""
# PATTERN_WALL_5X5 = """
# OOOOO
# OOOOO
# OOOOO
# OOOOO
# OOOOO
# """

# More minimalistic
PATTERN_WALL_5X5 = PATTERN_EMPTY_SPACE_5X5
CELL_CHAR_TO_PATTERN_5X5_STRINGS = {
    CELL_EMPTY_SPACE: PATTERN_EMPTY_SPACE_5X5,
    CELL_MIRROR_SLASH: PATTERN_MIRROR_SLASH_5X5,
    CELL_MIRROR_BACKSLASH: PATTERN_MIRROR_BACKSLASH_5X5,
    CELL_SPLITTER_V: PATTERN_SPLITTER_V_5X5,
    CELL_SPLITTER_H: PATTERN_SPLITTER_H_5X5,
    CELL_WALL: PATTERN_WALL_5X5,
}


@dataclass(kw_only=True)
class Viewer:
    problem_input_array: npt.NDArray[np.uint8]
    history: HistoryDictPerDepth
    display_size: tuple[int, int]
    simulation_step: int

    target_fps: int = 60
    min_luminance: int = 40
    max_luminance: int = 255 - min_luminance
    cell_width_px: int = 5
    running_game_loop: bool = True
    update_display: bool = False
    elapsed_frames: int = 0

    screen: pygame.SurfaceType = field(init=False)
    display_size_scaled: tuple[int, int] = field(init=False)
    mirror_surf: pygame.Surface = field(init=False)
    ray_array: npt.NDArray[np.uint8] = field(init=False)

    def init(self, title: str):
        pygame.init()
        self.display_size_scaled = (
            self.display_size[0] * self.cell_width_px,
            self.display_size[1] * self.cell_width_px,
        )
        self.screen = pygame.display.set_mode(self.display_size_scaled)
        pygame.display.set_caption(title)

    def start(self):
        self.init_mirror_surf()
        self.ray_array = self.generate_ray_array()

        initial_color = (self.min_luminance, self.min_luminance, self.min_luminance)
        self.screen.fill(initial_color)
        pygame.display.flip()

        clock = pygame.time.Clock()

        while self.running_game_loop:
            clock.tick(self.target_fps)
            self.consume_event_loop()
            if not self.update_display:
                continue
            self.update_ray_array(self.elapsed_frames)
            self.render()
            self.elapsed_frames += 1

        pygame.quit()

    def init_mirror_surf(self):
        mirror_array = self.generate_mirror_array()
        self.mirror_surf = pygame.surfarray.make_surface(mirror_array)
        self.mirror_surf.set_colorkey((0, 0, 0))

    def render(self):
        surf = pygame.surfarray.make_surface(self.ray_array)
        surf_scaled = pygame.transform.scale(surf, self.display_size_scaled)
        self.screen.blit(surf_scaled, (0, 0))
        self.screen.blit(self.mirror_surf, (0, 0))

        pygame.display.update()

    def update_ray_array(self, total_elapsed_frames: int) -> None:
        # Can give funny results
        # array = np.clip(array - 1, min_luminance, max_luminance)
        self.ray_array = np.where(
            self.ray_array > self.min_luminance,
            np.clip(self.ray_array * 0.99, 1.3 * self.min_luminance, 255),
            self.min_luminance,
        )
        for i in range(self.simulation_step):
            # All rays of same recursion depth move altogether at the same time
            history_for_depth = self.history[
                (i + self.simulation_step * total_elapsed_frames) % len(history)
            ]

            for history_line in history_for_depth:
                position = history_line[1]
                self.ray_array[position] = self.max_luminance

    def consume_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running_game_loop = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.update_display = not self.update_display
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  # XXX issue with AZERTY?
                    self.simulation_step += 1
                elif event.key == pygame.K_s:
                    self.simulation_step = (
                        self.simulation_step - 1 if self.simulation_step > 0 else 0
                    )
                elif event.key == pygame.K_SPACE:
                    self.update_display = not self.update_display
                elif event.key == pygame.K_r:
                    self.elapsed_frames = 0
                elif event.key == pygame.K_t:
                    self.elapsed_frames -= 12 * self.simulation_step
                elif event.key == pygame.K_g:
                    self.elapsed_frames += 12 * self.simulation_step

    def generate_ray_array(self) -> npt.NDArray[np.uint8]:
        return np.zeros(
            (self.display_size[0], self.display_size[1], 3), dtype=np.uint8
        ) + np.uint8(self.min_luminance)

    def generate_mirror_array(self) -> npt.NDArray[np.uint8]:
        mirror_array = np.zeros(
            (self.display_size_scaled[0], self.display_size_scaled[1], 3),
            dtype=np.uint8,
        )

        if self.cell_width_px == 3:
            empty = (
                parse_2d_string_array_to_uint8(PATTERN_EMPTY_SPACE_3X3) == CELL_WALL
            ) * 255
            slash = (
                parse_2d_string_array_to_uint8(PATTERN_MIRROR_SLASH_3X3) == CELL_WALL
            ) * 255
            backslash = (
                parse_2d_string_array_to_uint8(PATTERN_MIRROR_BACKSLASH_3X3)
                == CELL_WALL
            ) * 255
            splitter_v = (
                parse_2d_string_array_to_uint8(PATTERN_SPLITTER_V_3X3) == CELL_WALL
            ) * 255
            splitter_h = (
                parse_2d_string_array_to_uint8(PATTERN_SPLITTER_H_3X3) == CELL_WALL
            ) * 255
            full_wall = (
                parse_2d_string_array_to_uint8(PATTERN_WALL_3X3) == CELL_WALL
            ) * 255
        elif self.cell_width_px == 5:
            empty = (
                parse_2d_string_array_to_uint8(PATTERN_EMPTY_SPACE_5X5) == CELL_WALL
            ) * 255
            slash = (
                parse_2d_string_array_to_uint8(PATTERN_MIRROR_SLASH_5X5) == CELL_WALL
            ) * 255
            backslash = (
                parse_2d_string_array_to_uint8(PATTERN_MIRROR_BACKSLASH_5X5)
                == CELL_WALL
            ) * 255
            splitter_v = (
                parse_2d_string_array_to_uint8(PATTERN_SPLITTER_V_5X5) == CELL_WALL
            ) * 255
            splitter_h = (
                parse_2d_string_array_to_uint8(PATTERN_SPLITTER_H_5X5) == CELL_WALL
            ) * 255
            full_wall = (
                parse_2d_string_array_to_uint8(PATTERN_WALL_5X5) == CELL_WALL
            ) * 255
        else:
            raise NotImplementedError("Patterns only available for 3x3 or 5x5 cells")

        # Duplicate the pattern for all RGB coords along a new dim:
        # See https://stackoverflow.com/questions/32171917/how-to-copy-a-2d-array-into-a-3rd-dimension-n-times
        cell_char_to_pattern = {
            CELL_EMPTY_SPACE: np.repeat(empty[:, :, np.newaxis], 3, axis=2),
            CELL_MIRROR_SLASH: np.repeat(slash[:, :, np.newaxis], 3, axis=2),
            CELL_MIRROR_BACKSLASH: np.repeat(backslash[:, :, np.newaxis], 3, axis=2),
            CELL_SPLITTER_V: np.repeat(splitter_v[:, :, np.newaxis], 3, axis=2),
            CELL_SPLITTER_H: np.repeat(splitter_h[:, :, np.newaxis], 3, axis=2),
            CELL_WALL: np.repeat(full_wall[:, :, np.newaxis], 3, axis=2),
        }

        for row in range(self.problem_input_array.shape[0]):
            for col in range(self.problem_input_array.shape[1]):
                row_origin = self.cell_width_px * row
                col_origin = self.cell_width_px * col
                mirror_array[
                    row_origin : row_origin + self.cell_width_px,
                    col_origin : col_origin + self.cell_width_px,
                    :,
                ] = cell_char_to_pattern[self.problem_input_array[row, col]]

        return mirror_array


if __name__ == "__main__":
    problem = AdventOfCodeProblem202316()
    history_raw = json.loads(problem.get_output_log_part_1_file_path().read_text())
    history: History = [(h[0], tuple(h[1]), tuple(h[2])) for h in history_raw]  # type: ignore
    history_dict: HistoryDictPerDepth = defaultdict(list)
    for line in history:
        history_dict[line[0]].append(line)

    problem_input_array = problem.parse_input_text_file()

    # DONE
    # - Draw the mirrors. (for now problem_input_array is unused)
    #    For that, upscale to 3X3 tiles, and display rays as centered 1px lines
    # - Handle alpha, to have a "trace" effect
    viewer = Viewer(
        problem_input_array=problem_input_array,
        history=history_dict,
        display_size=(problem_input_array.shape[0], problem_input_array.shape[1]),
        simulation_step=4,
        # simulation_step=1,
    )
    viewer.init(f"AoC Y{problem.year} D{problem.day} | Click to Start")
    viewer.start()
