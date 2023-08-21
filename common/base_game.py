from common.scenes.dummy import run_dummy
from common.scenes.game_menu import game_menu
from common.scenes.game_ranking import game_ranking


class BaseGame:
    def __init__(self):
        pass

    def run(self):
        return NotImplemented

    def play(self):
        return NotImplemented

    @property
    def name(self):
        return NotImplemented

    def start(self):
        game_menu(self)

    def ranking(self):
        game_ranking(self)

    def instruction(self):
        return NotImplemented

    def get_scores(self):
        import random
        import string

        scores = [
            (
                random.randint(1, 1100),
                "".join(random.choices(string.ascii_letters, k=random.randint(4, 12))),
            )
            for _ in range(1, 15)
        ]
        scores = [x for x in sorted(scores, key=lambda x: x[0], reverse=True)]
        return scores

    def save_score(self, score):
        pass


class ExampleGame(BaseGame):
    def run(self):
        run_dummy()

    @property
    def name(self):
        return self.__class__
