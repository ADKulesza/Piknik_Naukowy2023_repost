import random
from pathlib import Path

import pygame

from common.components.core.app import App

app = App()
fort_size = 50
font_name = app.theme.font_name
font = pygame.font.Font(font_name, fort_size)


class Player:
    def __init__(self):
        app = App()
        paths = app.player.avatar.get_ufo_paths()
        player_img = pygame.image.load(paths[0]).convert_alpha()
        player_img = pygame.transform.scale(player_img, (128, 128))

        self.img = player_img
        self.X, self.Y = (app.canvas.get_width() // 2, app.canvas.get_height() - 110)
        self.rect = self.img.get_rect()
        self.rect.center = (self.X, self.Y)
        self.speed_left = -2
        self.speed_right = 4
        self.move = self.speed_left

    def update(self, screen):
        screen.blit(self.img, (self.rect.left, self.rect.top))


# Rocks
class Rock:
    def __init__(self):
        path_to_comet = Path(__file__).parent / "assets/kometa64.png"
        path_to_ship = Path(__file__).parent / "assets/statek_kosmiczny64.png"
        self.images = [path_to_comet, path_to_ship, path_to_ship, path_to_ship]
        img = random.choice(self.images)

        if img == path_to_ship:
            dims = (128, 128)
            speed = 3
        elif img == path_to_comet:
            dims = (192, 192)
            speed = 1
        img = pygame.image.load(img)
        img = pygame.transform.scale(img, dims)

        self.img = img
        self.move = speed * (1 + (random.random() - 0.5) / 10)
        self.rect = self.img.get_rect()
        self.X, self.Y = self.get_start_position()
        self.rect.center = (self.X, self.Y)

    def regenerate(self):
        self.rect.center = self.get_start_position()

    def update(self, screen):
        screen.blit(self.img, (self.rect.left, self.rect.top))

    def get_start_position(self):
        offset_x = 15
        pos_y = random.randint(-550, -200)
        pos_x = random.randint(offset_x, app.canvas.get_width() - offset_x)
        return pos_x, pos_y


# Score
class Score:
    def __init__(self):
        self.value = 0

        score_xy = (10, 10)

        self.text = font.render(f"Wynik: {self.value}", True, (255, 255, 255))
        (self.X, self.Y) = score_xy

    def update(self, screen):
        self.text = font.render(f"Wynik: {self.value}", True, (255, 255, 255))
        screen.blit(self.text, (self.X, self.Y))
