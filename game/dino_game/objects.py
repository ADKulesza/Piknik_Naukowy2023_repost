from pathlib import Path
from random import randint

import pygame

RECT_BOTTOM = 485


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load(
            Path(__file__).parent / "assets/player_walk_1.png"
        ).convert_alpha()
        player_walk2 = pygame.image.load(
            Path(__file__).parent / "assets/player_walk_2.png"
        ).convert_alpha()
        player_walk1 = pygame.transform.scale(player_walk1, (72 * 1.5, 84 * 1.5))
        player_walk2 = pygame.transform.scale(player_walk2, (72 * 1.5, 84 * 1.5))
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load(
            Path(__file__).parent / "assets/player_walk_2.png"
        ).convert_alpha()
        self.player_jump = pygame.transform.scale(
            self.player_jump, (72 * 1.5, 84 * 1.5)
        )

        self.image = self.player_walk[self.player_index]
        self.rect_bottom = RECT_BOTTOM

        self.rect = self.image.get_rect(midbottom=(400, self.rect_bottom))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound(
            Path(__file__).parent / "assets/audio_jump.mp3"
        )
        self.jump_sound.set_volume(0.25)

    def player_input(self):
        from common.components.core.app import App

        app = App()

        emg_move = app.get_emg_value() > app.player.mean

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or emg_move) and self.rect.bottom >= self.rect_bottom:
            self.gravity = -24.1
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.rect_bottom:
            self.rect.bottom = self.rect_bottom

    def animation_state(self):
        if self.rect.bottom < self.rect_bottom:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.rect_bottom = 483
        if type == "fly":
            fly1 = pygame.image.load(
                Path(__file__).parent / "assets/UFO1.png"
            ).convert_alpha()
            fly2 = pygame.image.load(
                Path(__file__).parent / "assets/UFO2.png"
            ).convert_alpha()
            fly1 = pygame.transform.scale(fly1, (438 / 2.8, 290 / 2.8))
            fly2 = pygame.transform.scale(fly2, (438 / 2.8, 290 / 2.8))
            self.frames = [fly1, fly2]
            y_pos = 260
        else:
            snail1 = pygame.image.load(
                Path(__file__).parent / "assets/alien1.png"
            ).convert_alpha()
            snail2 = pygame.image.load(
                Path(__file__).parent / "assets/alien2.png"
            ).convert_alpha()
            snail1 = pygame.transform.scale(snail1, (234 / 2.5, 327 / 2.5))
            snail2 = pygame.transform.scale(snail2, (234 / 2.5, 327 / 2.5))
            self.frames = [snail1, snail2]
            y_pos = self.rect_bottom
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1800, 2200), y_pos))

    def animation_state(self):
        if self.rect.bottom == 210:
            self.animation_index += 0.3
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
        else:
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def update(self, i):
        self.animation_state()
        self.rect.x -= i
        self.destroy()
        return int(i)

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
