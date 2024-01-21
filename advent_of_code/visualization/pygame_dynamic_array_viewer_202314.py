from dataclasses import dataclass, field
from typing import override

import click
import numpy as np
import pygame
import xarray as xr

from advent_of_code.visualization.protocols import (
    AOCPygameVisualizer,
    AOCPygameVisualizerFactory,
)
from advent_of_code.year_2023.year_2023_day_14 import AdventOfCodeProblem202314


@click.command
@click.option(
    "--choice",
    help="Choice of mode of execution of the file",
    type=click.Choice(
        [
            "solve",
            "generate_visualizations_instructions",
            "visualize",
        ]
    ),
    required=True,
    default="visualize",
)
@click.option(
    "--part",
    help="Problem part to solve/visualize",
    type=click.Choice(["one", "two", "both", "irrelevant"]),
    required=True,
    default="both",
)
def main(choice: str, part: str):
    if choice == "solve":
        print(
            AdventOfCodeProblem202314().solve(
                part_1=part in {"one", "both"}, part_2=part in {"two", "both"}
            )
        )
    elif choice == "generate_visualizations_instructions":
        # Only part 2 is animation-worth material
        AdventOfCodeProblem202314().write_visualizations_instructions_for_part_2()
    elif choice == "visualize":
        visualizer = AOCPygameVisualizerFactory202314().create_visualizer()
        visualizer.start()
    else:
        click.secho("Invalid choice", err=True)


# [visu] Moving Rocks (moving rocks)


@dataclass(kw_only=True)
class AOCVisualizer202314(AOCPygameVisualizer):
    history: xr.DataArray
    simulation_step: int

    updates_per_second: int = 1
    min_luminance: int = 40
    max_luminance: int = 255 - min_luminance

    _board_array_surf: pygame.Surface = field(init=False)
    _rocks_xda: xr.DataArray = field(init=False)

    @override
    def init_state(self):
        self._init_board_surf()

    @override
    def update_state(self) -> None:
        self._update_rocks_xda(self.elapsed_frames)

    @override
    def update_surfaces(self):
        surf = pygame.surfarray.make_surface(self._rocks_xda.values)
        surf_scaled = pygame.transform.scale(surf, self.display_size)
        self.screen.blit(surf_scaled, (0, 0))
        self.screen.blit(self._board_array_surf, (0, 0))

    @override
    def consume_event(self, event: pygame.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.update_simulation = not self.update_simulation
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Potentiel issue with AZERTY keyboards?
                self.simulation_step += 1
            elif event.key == pygame.K_s:
                self.simulation_step = (
                    self.simulation_step - 1 if self.simulation_step > 0 else 0
                )
            elif event.key == pygame.K_SPACE:
                self.update_simulation = not self.update_simulation
            elif event.key == pygame.K_r:
                self.elapsed_frames = 0
            elif event.key == pygame.K_t:
                self.elapsed_frames -= 12 * self.simulation_step
            elif event.key == pygame.K_g:
                self.elapsed_frames += 12 * self.simulation_step

    def _init_board_surf(self):
        board_array = self._generate_board_array()
        self._board_array_surf = pygame.surfarray.make_surface(board_array.values)
        self._board_array_surf = pygame.transform.scale(
            self._board_array_surf, self.display_size
        )
        self._board_array_surf.set_colorkey((0, 0, 0))

    def _update_rocks_xda(self, total_elapsed_frames: int) -> None:
        if total_elapsed_frames % (self.target_fps // self.updates_per_second) != 0:
            return
        for i in range(self.simulation_step):
            time = (
                i
                + self.simulation_step
                * (total_elapsed_frames // (self.target_fps // self.updates_per_second))
            ) % self.history["time"].size

            print(time)
            channel = (self.history.isel(time=time) == ord("O")).astype(np.uint8)
            self._rocks_xda = xr.concat(
                [channel * 128, channel * 128, channel * 255], dim="color"
            ).transpose(..., "color")

    def _generate_board_array(self) -> xr.DataArray:
        channel = ((self.history.isel(time=0) == ord("#")) * 200).astype(np.uint8)
        return xr.concat([channel, channel, channel], dim="color").transpose(
            ..., "color"
        )


class AOCPygameVisualizerFactory202314(AOCPygameVisualizerFactory):
    def create_visualizer(self) -> AOCVisualizer202314:
        problem = AdventOfCodeProblem202314()

        # Create if not exists
        if not problem.get_visualizations_instructions_for_part_2_file_path().exists():
            problem.write_visualizations_instructions_for_part_2()

        history_xda = self.read_history(problem)

        viewer = AOCVisualizer202314(
            title=f"AoC Y{problem.year} D{problem.day} | Click to Start",
            simulation_size=(
                history_xda["row"].size,
                history_xda["col"].size,
            ),
            history=history_xda,
            simulation_step=1,
            updates_per_second=2,
        )
        return viewer

    @staticmethod
    def read_history(problem: AdventOfCodeProblem202314) -> xr.DataArray:
        return xr.open_zarr(
            problem.get_visualizations_instructions_for_part_2_file_path()
        )["board_history"].compute()


if __name__ == "__main__":
    main()  # type: ignore
