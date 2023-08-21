import time

import numpy as np
import pygame


def run_dummy(t=5):
    from common.components.core.app import App

    game = App()
    canvas = game.canvas

    run = True
    color = (255, 255, 255)

    start = time.time()

    while run:
        canvas.fill(color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        rect_color = np.random.randint(0, 255, 3)
        pygame.draw.rect(
            canvas,
            rect_color,
            pygame.Rect(0, 0, *pygame.display.get_surface().get_size()),
        )
        pygame.display.update()
        if time.time() - start > t:
            run = False
