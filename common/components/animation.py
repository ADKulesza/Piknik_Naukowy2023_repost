import time
from itertools import cycle
from pathlib import Path

import pygame


class Animation:
    def __init__(self, path, delay=100, dimensions=None):
        frames = Path(path)
        imgs = [pygame.image.load(path).convert() for path in sorted(frames.glob("*"))]
        if dimensions:
            imgs = [pygame.transform.scale(img, dimensions) for img in imgs]
        self.imgs = cycle(imgs)

        self.last_update_time = time.time()
        self.frame = next(self.imgs)
        self.delay_ms = delay

    def update(self, canvas):
        if time.time() - self.last_update_time > self.delay_ms / 1000:
            self.frame = next(self.imgs)
            self.last_update_time = time.time()
        canvas.blit(self.frame, (0, 0))
