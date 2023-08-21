from pathlib import Path

from common.components.background_animation import BackgroundAnimation
from common.utils import singleton


@singleton
class GalaxyBackground(BackgroundAnimation):
    def __init__(self):
        frames = Path(__file__).parent / "static/galaxy"
        super().__init__(path=frames)
