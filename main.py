import signal

from amplifiers.drivers.debug.debug_amplifier import DummyAmplfier
from amplifiers.drivers.tmsi.tmsi import TMSI
from common.components.core.app import App
from game.dino_game.game1 import Game1
from game.game3.game3 import Game3
from game.quiz.quiz import Quiz
from game.wrestler.wrestler import Wrestler


def signal_handler(sig, frame):
    from common.components.button import ExitButton

    print("You pressed Ctrl+C!")
    ExitButton.exit()


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


game = App()
try:
    game.add_amplifier(TMSI)
except ValueError as e:
    print(e)
    print("Gramy bez wzmacniacza!")
    game.add_amplifier(DummyAmplfier)

game.add_game(Game1)
game.add_game(Wrestler)
game.add_game(Game3)
game.add_game(Quiz)

game.start()
