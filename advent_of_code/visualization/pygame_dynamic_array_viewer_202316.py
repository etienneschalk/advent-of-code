import json
from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt
import pygame

from advent_of_code.year_2023.year_2023_day_16 import AdventOfCodeProblem202316

type HistoryLine = tuple[int, tuple[int, int], tuple[int, int]]
type History = tuple[HistoryLine, ...]


@dataclass(kw_only=True)
class Viewer:
    update_func: npt.NDArray[np.uint8]
    history: History
    display_size: tuple[int, int]
    fps: int
    display: pygame.SurfaceType = field(init=False)
    display_size_3x: tuple[int, int] = field(init=False)
    simulation_step: int

    def init(self, title: str):
        pygame.init()
        self.display_size_3x = self.display_size[0] * 3, self.display_size[1] * 3
        self.display = pygame.display.set_mode(self.display_size_3x)
        pygame.display.set_caption(title)

    def start(self):
        array = np.zeros(
            (self.display_size[0], self.display_size[1], 3), dtype=np.uint8
        )
        running = True
        total_elapsed_frames = 0
        clock = pygame.time.Clock()

        display_update = False
        while running:
            clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    display_update = not display_update
            if not display_update:
                continue

            for i in range(self.simulation_step):
                history_line = history[
                    (i + self.simulation_step * total_elapsed_frames) % len(history)
                ]
                position = history_line[1]
                array[position] = 255

            surf = pygame.surfarray.make_surface(array)
            surf_3x = pygame.transform.scale(surf, self.display_size_3x)
            self.display.blit(surf_3x, (0, 0))
            pygame.display.update()

            total_elapsed_frames += 1

        pygame.quit()


if __name__ == "__main__":
    problem = AdventOfCodeProblem202316()
    history_raw = json.loads(problem.get_output_log_part_1_file_path().read_text())
    history: History = [(h[0], tuple(h[1]), tuple(h[2])) for h in history_raw]  # type: ignore
    problem_input_array = problem.parse_input_text_file()

    # TODO:
    # - Draw the mirrors. (for now problem_input_array is unused)
    #    For that, upscale to 3x3 tiles, and display rays as centered 1px lines
    # - Handle alpha, to have a "trace" effect
    viewer = Viewer(
        update_func=problem_input_array,
        history=history,
        display_size=(problem_input_array.shape[0], problem_input_array.shape[1]),
        fps=60,
        simulation_step=40,
    )
    viewer.init(f"AoC Y{problem.year} D{problem.day} | Click to Start")
    viewer.start()
