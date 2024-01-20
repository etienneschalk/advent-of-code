from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol

import pygame


@dataclass(kw_only=True)
class AOCPygameVisualizer:
    # Opinionated visualizer, adapted to display "square cells"

    # Title displayed in Window
    title: str
    # Simulation Array size
    simulation_size: tuple[int, int]

    target_fps: int = 60
    running_game_loop: bool = True
    elapsed_frames: int = 0
    # Skip the game loop if none (pausing the simulation + rendering)
    update_simulation: bool = False
    cell_width_in_px: int = 5

    screen: pygame.SurfaceType = field(init=False)
    # Actual scaled display size using cell_width_in_px
    display_size: tuple[int, int] = field(init=False)

    @abstractmethod
    def init_state(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_state(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_surfaces(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def consume_event(self, event: pygame.Event) -> None:
        raise NotImplementedError

    def consume_event_loop(self):
        for event in pygame.event.get():
            # All visualizers should be quittable
            if event.type == pygame.QUIT:
                self.running_game_loop = False
            self.consume_event(event)

    def init(self):
        self.display_size = (
            self.simulation_size[0] * self.cell_width_in_px,
            self.simulation_size[1] * self.cell_width_in_px,
        )
        self.screen = pygame.display.set_mode(self.display_size)
        pygame.display.set_caption(self.title)
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

        self.init_state()

    def start(self):
        self.init()

        clock = pygame.time.Clock()
        while self.running_game_loop:
            clock.tick(self.target_fps)

            self.consume_event_loop()
            if not self.update_simulation:
                continue

            self.update_state()
            self.update_surfaces()

            pygame.display.flip()
            self.elapsed_frames += 1

        pygame.quit()


class AOCPygameVisualizerFactory(Protocol):
    @abstractmethod
    def create_visualizer(self) -> AOCPygameVisualizer:
        raise NotImplementedError
