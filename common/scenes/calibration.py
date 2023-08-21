import os
import time

import numpy as np
import pandas as pd
import pygame

from common.components.calibration_background import CalibrationBackground

TEXT_COLOR = (255, 255, 255)


def calibration():
    TEXT_PATH = os.path.join(
        os.getcwd(), "common", "scenes", "calibration_display_text.csv"
    )
    from common.components.core.app import App

    display_text = pd.read_csv(TEXT_PATH)
    app = App()

    screen = app.canvas
    theme = app.theme

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    font = pygame.font.Font(theme.font_name, int(theme.font_size * 2))
    major_font = pygame.font.Font(theme.font_name, int(theme.font_size * 4))

    # screen.fill(app.theme.primary_color)
    background = CalibrationBackground()
    background.update(screen)
    pygame.display.update()

    thresholds = []

    delay = 2

    for idx, row in display_text.iterrows():
        if row.stage < 0:
            continue
        st_time = time.time()
        # Tutaj odpalam kalibracje w zależności od row.stage

        background.update(screen)

        calib_text = major_font.render("KAlIBRACJA", True, TEXT_COLOR)
        calib_text_rect = calib_text.get_rect(
            center=(screen_width / 2, screen_height / 10)
        )
        screen.blit(calib_text, calib_text_rect)

        emg_sampels = []

        screen_text = row.text.split(".")
        for _line, _t in enumerate(screen_text, 0):
            text = font.render(_t, True, TEXT_COLOR)
            text_rect = text.get_rect(
                midleft=(screen_width / 32, screen_height / (2.5 - _line / 2))
            )
            screen.blit(text, text_rect)

        pygame.display.update()
        time.sleep(delay)
        while time.time() - st_time < row.duration + delay:
            if row.stage > 0:
                emg_sampels.append(app.get_emg_value())
                print(emg_sampels[-1])
            app.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        return None

        if emg_sampels:
            threshold = np.mean(emg_sampels)
            thresholds.append(threshold)

    min_, mean, max_ = thresholds

    if 0 < min_ < mean < max_:
        return min_, mean, max_
    else:
        # Błąd w kalibracji
        background.update(screen)
        error_display = display_text[display_text.stage == -1]

        for idx, row in error_display.iterrows():
            screen_text = row.text.split(".")
            for _line, _t in enumerate(screen_text, 0):
                text = font.render(_t, True, TEXT_COLOR)
                text_rect = text.get_rect(
                    midleft=(screen_width / 32, screen_height / (2.5 - _line / 2))
                )
                screen.blit(text, text_rect)

            pygame.display.update()
            time.sleep(delay)
        calibration()
