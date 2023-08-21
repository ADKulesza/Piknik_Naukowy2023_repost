import pygame

from common.components.button import Button
from common.components.galaxy_background import GalaxyBackground


def game_menu(game):
    from common.components.core.app import App

    app = App()
    screen = app.canvas
    buttons = []
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    background = GalaxyBackground()
    background.update(screen)
    pygame.display.update()

    button_rect = (0, 0, 300, 75)

    function = game.run
    buttons.append(Button(button_rect, function, value="Graj"))
    function = game.ranking
    buttons.append(Button(button_rect, function, value="Ranking"))
    function = game.instruction
    buttons.append(Button(button_rect, function, value="Instrukcja"))
    back = Button(button_rect, None, value="Powrót")
    buttons.append(back)

    for i, button in enumerate(buttons, 1):
        button.rect.center = (screen_width / 2, i / (len(buttons) + 1) * screen_height)

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
