import pygame

from common.components.button import Button
from common.components.ranking_background import RankingBackground
from common.components.ranking_score import Score, ScoreHeader


def rankings():
    from common.components.core.app import App

    background = RankingBackground()

    app = App()
    screen = app.canvas
    games = list(app.games)

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    screen.fill(app.theme.primary_color)
    background.update(screen)
    pygame.display.update()

    rect_dims = (0, 0, 800, 46)
    back = Button(rect_dims, None, value="Powrót")

    idx = 0
    pre_idx = None
    elements = []

    while not back.clicked:
        if idx != pre_idx:
            game = games[idx]

            elements = []

            scores = game.get_scores()[:10]

            elements.append(ScoreHeader(rect_dims, data=f"{game.name}"))
            for i, (score, name) in enumerate(scores, 1):
                data = {"position": i, "score": score, "name": name}
                score = Score(rect_dims, data=data)
                elements.append(score)

            elements.append(back)

            for i, element in enumerate(elements, 1):
                element.rect.center = (
                    screen_width / 2,
                    i / (len(elements) + 2) * screen_height,
                )

            pre_idx = idx

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

            for element in elements:
                element.check_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    idx -= 1
                if event.key == pygame.K_RIGHT:
                    idx += 1

        idx %= len(games)

        screen.fill(app.theme.primary_color)
        background.update(screen)
        for element in elements:
            element.update(screen)
        pygame.display.update()
        app.tick()
