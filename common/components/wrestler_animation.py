import time
from itertools import cycle

import pygame

from common.components.animation import Animation
from common.utils import singleton


@singleton
class WrestlerAnimation(Animation):
    def __init__(self, frame_paths, delay=500, dimensions=None, position=(0, 0)):
        imgs = [pygame.image.load(path).convert_alpha() for path in frame_paths]
        if dimensions:
            imgs = [
                pygame.transform.scale(img, dimensions).convert_alpha() for img in imgs
            ]
        self.low, self.high = imgs
        self.imgs = cycle(imgs)

        self.last_update_time = time.time()
        self.frame = next(self.imgs)
        self.delay_ms = delay

        self.position = position

    def update(self, canvas):
        pos = self.frame.get_rect(center=self.position)
        if time.time() - self.last_update_time > self.delay_ms / 1000:
            self.frame = next(self.imgs)
            self.last_update_time = time.time()

        canvas.blit(self.frame, pos)
