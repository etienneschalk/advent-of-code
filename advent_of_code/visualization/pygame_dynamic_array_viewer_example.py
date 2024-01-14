from typing import Callable

import numpy as np
import numpy.typing as npt
import pygame

# See https://karthikkaranth.me/blog/drawing-pixels-with-python/

type PureSideEffect = Callable[[], npt.NDArray[np.uint8]]


class Viewer:
    def __init__(self, update_func: PureSideEffect, display_size: tuple[int, int]):
        self.update_func = update_func
        pygame.init()
        self.display = pygame.display.set_mode(display_size)

    def set_title(self, title: str):
        pygame.display.set_caption(title)

    def start(self):
        running = True
        fps = 60
        total_elapsed_frames = 0
        clock = pygame.time.Clock()
        while running:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.inner_game_loop(total_elapsed_frames)
            pygame.display.update()

            total_elapsed_frames += 1

        pygame.quit()

    def inner_game_loop(self, total_elapsed_frames: int):
        array = self.update_func()
        surf = pygame.surfarray.make_surface(array)
        self.display.blit(surf, (0, 0))


def update_with_random_array():
    image = np.random.random((600, 600, 3)) * 255.0
    image[:, :200, 0] = 255.0
    image[:, 200:400, 1] = 255.0
    image[:, 400:, 2] = 255.0
    return image.astype(np.uint8)


if __name__ == "__main__":
    viewer = Viewer(update_with_random_array, (600, 600))
    viewer.start()
