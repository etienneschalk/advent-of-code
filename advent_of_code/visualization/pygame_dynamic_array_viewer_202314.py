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

    state_updates_per_second: int = 1
    min_luminance: int = 40
    max_luminance: int = 255 - min_luminance

    _board_array_surf: pygame.Surface = field(init=False)
    _rocks_xda: xr.DataArray = field(init=False)

    @override
    def init(self):
        self.display_size = (
            self.simulation_size[0] * self.cell_width_in_px,
            self.simulation_size[1] * self.cell_width_in_px,
        )
        self.screen = pygame.display.set_mode(
            (self.display_size[0] * 1.5, self.display_size[1] * 1.5)
        )
        pygame.display.set_caption(self.title)
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

        self.init_state()

    @override
    def init_state(self):
        self._init_board_surf()

    @override
    def update_state(self) -> None:
        self._update_rocks_xda()

    @override
    def update_surfaces(self):
        self.screen.fill((0, 0, 0))

        in_between_frames = self.target_fps // self.state_updates_per_second
        angle_in_degrees = -25 + (
            (90) * (self.elapsed_frames % (in_between_frames * 4)) / in_between_frames
        )

        surf = pygame.surfarray.make_surface(self._rocks_xda.values)
        surf_scaled = pygame.transform.scale(surf, self.display_size)
        surf_scaled.set_colorkey((0, 255, 0))
        w, h = pygame.display.get_surface().get_size()
        old_rect = surf_scaled.get_rect(center=(w // 2, h // 2))
        surf_scaled, new_rect = rot_center(surf_scaled, old_rect, angle_in_degrees)
        self.screen.blit(surf_scaled, new_rect)

        surf = self._board_array_surf
        surf.set_colorkey((0, 0, 0))
        w, h = pygame.display.get_surface().get_size()
        old_rect = surf.get_rect(center=(w // 2, h // 2))
        surf, new_rect = rot_center(surf, old_rect, angle_in_degrees)
        self.screen.blit(surf, new_rect)

    @override
    def consume_event(self, event: pygame.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.update_simulation = not self.update_simulation
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.update_simulation = not self.update_simulation
            elif event.key == pygame.K_r:
                self.elapsed_frames = 0
            elif event.key == pygame.K_t:
                self.elapsed_frames -= self.target_fps // self.state_updates_per_second
            elif event.key == pygame.K_g:
                self.elapsed_frames += self.target_fps // self.state_updates_per_second

    def _init_board_surf(self):
        board_array = self._generate_board_array()
        self._board_array_surf = pygame.surfarray.make_surface(board_array.values)
        self._board_array_surf = pygame.transform.scale(
            self._board_array_surf, self.display_size
        )
        self._board_array_surf.set_colorkey((0, 0, 0))

    def time(self, i: int) -> int:
        time = (
            i
            + self.simulation_step
            * (
                self.elapsed_frames
                // (self.target_fps // self.state_updates_per_second)
            )
        ) % self.history["time"].size
        return time

    def _update_rocks_xda(self) -> None:
        if (
            self.elapsed_frames % (self.target_fps // self.state_updates_per_second)
            != 0
        ):
            return
        for i in range(self.simulation_step):
            time = self.time(i)
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


def rot_center(image: pygame.Surface, rect: pygame.Rect, angle: float):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


# TODO eschalk use pymunk
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
            state_updates_per_second=1,
        )
        return viewer

    @staticmethod
    def read_history(problem: AdventOfCodeProblem202314) -> xr.DataArray:
        return xr.open_zarr(
            problem.get_visualizations_instructions_for_part_2_file_path()
        )["board_history"].compute()


if __name__ == "__main__":
    main()  # type: ignore
