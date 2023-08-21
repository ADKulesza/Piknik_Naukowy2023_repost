import pygame

from common.components.button import Button
from common.components.galaxy_background import GalaxyBackground


def select_game():
    from common.components.core.app import App

    app = App()

    background = GalaxyBackground()

    screen = app.canvas
    games = app.games

    buttons = []

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    background.update(screen)
    pygame.display.update()

    button_rect = (0, 0, 360, 75)

    for i, game in enumerate(games, 1):
        function = game.start
        button = Button(button_rect, function, value=game.name)
        button.rect.center = (screen_width / 2, i / (len(games) + 2) * screen_height)
        buttons.append(button)

    back = Button(button_rect, None, value="Powrót")
    back.rect.center = (screen_width / 2, (i + 1) / (len(games) + 2) * screen_height)
    buttons.append(back)

    while not back.clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

            for button in buttons:
                button.check_event(event)

        background.update(screen)
        for button in buttons:
            button.update(screen)
        pygame.display.update()
        app.tick()
