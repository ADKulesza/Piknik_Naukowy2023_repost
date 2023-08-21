from pathlib import Path

from common.components.animation import Animation
from common.utils import singleton


@singleton
class CalibrationBackground(Animation):
    def __init__(self):
        frames = Path(__file__).parent / "static/calibration"
        super().__init__(path=frames, delay=1)
