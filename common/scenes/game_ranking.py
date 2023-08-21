import pygame

from common.components.button import Button
from common.components.ranking_background import RankingBackground
from common.components.ranking_score import Score, ScoreHeader


def game_ranking(game, add_exit=True):
    from common.components.core.app import App

    app = App()
    screen = app.canvas
    elements = []
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    screen.fill(app.theme.primary_color)
    background = RankingBackground()
    background.update(screen)

    pygame.display.update()

    scores = game.get_scores()[:10]

    rect_dims = (0, 0, 800, 46)

    elements.append(ScoreHeader(rect_dims))
    for i, (score, name) in enumerate(scores, 1):
        data = {"position": i, "score": score, "name": name}
        score = Score(rect_dims, data=data)
        elements.append(score)
    if add_exit:
        back = Button(rect_dims, None, value="Powrót")
        elements.append(back)

    for i, element in enumerate(elements, 1):
        element.rect.center = (
            screen_width / 2,
            i / (len(elements) + 2) * screen_height,
        )

    while not back.clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

            for element in elements:
                element.check_event(event)

        screen.fill(app.theme.primary_color)
        background.update(screen)
        for element in elements:
            element.update(screen)
        pygame.display.update()
        app.tick()
