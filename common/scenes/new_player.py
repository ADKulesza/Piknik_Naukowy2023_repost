import time
from collections import namedtuple

import pygame

from amplifiers.drivers.debug.debug_amplifier import DummyAmplfier
from common.components.button import AvatarChoiceButton
from common.components.galaxy_background import GalaxyBackground
from common.components.input import TextInputBox
from common.components.select_avatar import SelectAvatar
from common.scenes.calibration import calibration

Player = namedtuple("Player", ["name", "min", "mean", "max", "avatar"])


def new_player():
    from common.components.core.app import App

    app = App()
    screen = app.canvas
    theme = app.theme

    background = GalaxyBackground()

    main_font = pygame.font.Font(theme.font_name, theme.font_size * 3)
    minor_font = pygame.font.Font(theme.font_name, theme.font_size * 2)
    mini_font = pygame.font.Font(theme.font_name, int(theme.font_size * 0.7))
    background.update(screen)
    pygame.display.flip()

    screen_width = screen.get_width()
    screen_height = screen.get_height()
    text_input_box = TextInputBox(screen_width / 2, screen_height / 2, 400, main_font)

    player_avatar = SelectAvatar()

    while not text_input_box.done:
        app.clock.tick(60)
        for event in pygame.event.get():
            text_input_box.check_event(event)

        background.update(screen)
        text_input_box.update(screen)
        pygame.display.flip()

    background.update(screen)

    player_name = text_input_box.value
    text = f"Witaj {player_name}!"
    text = main_font.render(text, True, theme.secondary_color)

    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # ------- Wybór postaci -------
    time.sleep(1)

    text = "Wybierz swoją postać!"
    background.update(screen)

    text = minor_font.render(text, True, theme.secondary_color)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    time.sleep(2)
    background.update(screen)
    buttons = []
    avatars_img = []
    for av_name in player_avatar.avatar_choices.keys():
        buttons.append(
            AvatarChoiceButton(
                (0, 0, 250, 75), player_avatar.set_avatar, value=av_name, font=mini_font
            )
        )

        _av_path = player_avatar.get_avatar_path(av_name)
        _img = pygame.image.load(_av_path).convert_alpha()

        avatars_img.append(_img)

    for i, button in enumerate(buttons, 1):
        button.rect.center = (
            i / (len(buttons) + 1) * screen_width,
            screen_height * 7 / 8,
        )

    av_rect_list = []
    for i, _img in enumerate(avatars_img, 1):
        _av_rect = _img.get_rect(
            center=(i / (len(avatars_img) + 1) * screen_width, screen_height * 1 / 2)
        )
        av_rect_list.append(_av_rect)
        screen.blit(_img, _av_rect)

    run = 1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

            for button in buttons:
                button.check_event(event)
                if button.clicked:
                    run = 0

        for button in buttons:
            button.update(screen)
        pygame.display.update()
        app.tick()

    # ------- Koniec wyboru postaci -------
    time.sleep(0.5)

    thresholds = None
    if isinstance(app.amplifier.amp, DummyAmplfier):
        thresholds = 1, 5, 9
    else:
        thresholds = calibration()

    if not thresholds:
        return

    player = Player(player_name, *thresholds, player_avatar)
    app.player = player

    text = f"Graj jako {app.player.name}"
    font = pygame.font.Font(app.theme.font_name, app.theme.font_size)

    text = font.render(text, True, "BLACK")
    app.menu_button_width = text.get_rect().width + 50
