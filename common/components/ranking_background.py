from pathlib import Path

from common.components.animation import Animation
from common.utils import singleton


@singleton
class RankingBackground(Animation):
    def __init__(self):
        path = Path(__file__).parent / "static/ranking"

        from common.components.core.app import App

        super().__init__(path=path, dimensions=App().dimensions)
