import colorsys
import time
from pathlib import Path

import pygame

from amplifiers.drivers.debug.debug_amplifier import DummyAmplfier
from common.base_game import BaseGame
from common.components.core.app import App
from common.components.wrestler_animation import WrestlerAnimation
from common.utils import singleton


@singleton
class Wrestler(BaseGame):
    name = "Strongman"

    def __init__(self):
        super().__init__()
        app = App()

        # progression bar
        self.progress_bar_max_width = 400
        self.progress_bar_height = 30

        # screen & player
        background_img_path = Path(__file__).parent / "background.png"
        background_img = pygame.image.load(background_img_path).convert_alpha()
        self.background_img = pygame.transform.scale(background_img, app.dimensions)
        pygame.display.set_caption("Wrestling Game")
        self.player_anim = None

        self.time_to_hold = 15

    def run(self):
        self.wrestle()

    def wrestle(self):
        app = App()

        font_name = app.theme.font_name
        font_size = 50
        font = pygame.font.Font(font_name, font_size)

        self.player_anim = WrestlerAnimation(
            app.player.avatar.get_sztanga_paths(),
            position=(
                app.canvas.get_rect().width // 2,
                app.canvas.get_rect().height // 2,
            ),
        )

        screen = app.canvas

        # wait for start
        ready_to_curl = False
        while not ready_to_curl:
            for event in pygame.event.get():
                # exit
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    # exit
                    if event.key == pygame.K_p:
                        return
                    # start game
                    if event.key == pygame.K_SPACE:
                        ready_to_curl = True

            screen.blit(self.background_img, (0, 0))

            pose = self.player_anim.low
            position = pose.get_rect(center=self.player_anim.position)
            screen.blit(pose, position)

            hint_img = font.render(
                "Naciśnij spacje aby rozpocząć", True, app.theme.primary_color
            )
            hint_img_rect = hint_img.get_rect()
            hint_img_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
            screen.blit(hint_img, hint_img_rect)

            pygame.display.update()
            app.tick()

        # wait for user to start
        curling = False

        screen.blit(self.background_img, (0, 0))

        pygame.display.update()
        while not curling:
            for event in pygame.event.get():
                # exit
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    # exit
                    if event.key == pygame.K_p:
                        return
                    # start game
                    elif event.key == pygame.K_v:
                        curling = True
            screen.blit(self.background_img, (0, 0))

            pose = self.player_anim.low
            position = pose.get_rect(center=self.player_anim.position)
            screen.blit(pose, position)

            hint_text = (
                "Zaciśnij mięśnie!"
                if not isinstance(app.amplifier.amp, DummyAmplfier)
                else "Przytrzymaj przycisk v"
            )
            hint_img = font.render(hint_text, True, app.theme.primary_color)
            hint_img_rect = hint_img.get_rect()
            hint_img_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
            screen.blit(hint_img, hint_img_rect)
            pygame.display.update()

        # właściwa część gry
        pygame.display.update()
        start_time = time.time()
        play_time = 0
        while curling and (play_time < self.time_to_hold):
            for event in pygame.event.get():
                # exit
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    # exit
                    if event.key == pygame.K_p:
                        return

            # ścikanie/wciskanie
            keys = pygame.key.get_pressed()
            key_pressed = keys[pygame.K_v]

            # TODO DODAĆ LEPSZĄ FUNKCJĘ ŚCISKANIA MIĘŚNI
            emg_move = app.get_emg_value() > app.player.mean

            curling = key_pressed or emg_move

            play_time = time.time() - start_time
            time_to_win = self.time_to_hold - play_time
            screen.blit(self.background_img, (0, 0))
            self.draw_progress_bar(time_to_win)
            app.tick()
            self.player_anim.update(screen)

            pygame.display.update()

        score = int(round(play_time, 2) * 100)
        score = min(score, self.time_to_hold * 100)

        screen.blit(self.background_img, (0, 0))

        pose = self.player_anim.low
        position = pose.get_rect(center=self.player_anim.position)
        screen.blit(pose, position)

        score_text = f"Twój wynik to {score}!"
        if play_time >= self.time_to_hold:
            score_text = f"Wygrałeś! {score_text}"
        hint_img = font.render(score_text, True, app.theme.primary_color)
        hint_img_rect = hint_img.get_rect()
        hint_img_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        screen.blit(hint_img, hint_img_rect)
        pygame.display.update()
        self.save_score(score)

        time.sleep(4)

    def draw_progress_bar(self, remaining_time):
        app = App()
        progress_width = max(
            0, int((remaining_time / self.time_to_hold) * self.progress_bar_max_width)
        )

        progress_rect = pygame.Rect(
            0,
            0,
            progress_width,
            self.progress_bar_height,
        )
        progress_rect.center = (app.canvas.get_width() // 2, 50)

        # bar color change
        progress_color = self.interpolate_color(1 - remaining_time / self.time_to_hold)

        pygame.draw.rect(app.canvas, progress_color, progress_rect)

    @staticmethod
    def interpolate_color(t):
        red_hsv = (0, 1, 1)
        green_hsv = (1 / 3, 1, 1)

        hue = red_hsv[0] + (green_hsv[0] - red_hsv[0]) * t
        interpolated_hsv = (hue, 1, 1)

        r, g, b = colorsys.hsv_to_rgb(*interpolated_hsv)

        return int(r * 255), int(g * 255), int(b * 255)
