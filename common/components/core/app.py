import pygame

from amplifiers.amplifier import MainAmp
from common.components.button import Button, ExitButton
from common.components.galaxy_background import GalaxyBackground
from common.scenes.new_player import new_player
from common.scenes.rankings import rankings
from common.scenes.select_game import select_game
from common.signal_processing.rms import RMS
from common.themes.theme import Theme
from common.utils import singleton

pygame.init()


@singleton
class App:
    dimensions = (1300, 710)

    def __init__(self):
        self.games = []

        self.theme = Theme("common/themes/base.yaml")

        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.player = None

        self.canvas = pygame.display.set_mode(self.dimensions)
        pygame.display.set_caption("Moja Gra")

        self.menu_button_width = 400
        self.amplifier = None
        self.rms = None

        self.prepare()

        from common.scenes.new_player import Player

        self.player = Player("test", 1, 2, 3, "einstein")

    def get_emg_value(self, samples=128):
        return self.rms.get_rms(samples)

    def prepare(self):
        pass

    def add_game(self, game):
        self.games.append(game())
        self.games = list(sorted(set(self.games), key=lambda g: g.name))

    def add_amplifier(self, driver):
        self.amplifier = MainAmp(driver)
        self.rms = RMS(self.amplifier)

    def start(self):
        background = GalaxyBackground()

        previous_player = self.player

        screen_width = self.canvas.get_width()
        screen_height = self.canvas.get_height()

        button_height = 75
        button_widht = self.menu_button_width

        buttons = []

        b1 = Button((0, 0, button_widht, button_height), new_player, value="Nowy gracz")
        b1.rect.center = (screen_width / 2, 1 / 5 * screen_height)
        buttons.append(b1)

        b2 = Button(
            (0, 100, button_widht, button_height),
            select_game,
            value="Brak gracza",
            disabled=True,
        )
        b2.rect.center = (screen_width / 2, 2 / 5 * screen_height)
        buttons.append(b2)

        b3 = Button((0, 200, button_widht, button_height), rankings, value="Ranking")
        b3.rect.center = (screen_width / 2, 3 / 5 * screen_height)
        buttons.append(b3)

        b4 = ExitButton((0, 300, button_widht, button_height))
        b4.rect.center = (screen_width / 2, 4 / 5 * screen_height)
        buttons.append(b4)

        run = True
        while run:
            self.canvas.fill(self.theme.primary_color)
            background.update(self.canvas)
            for button in buttons:
                button.update(self.canvas)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                for button in buttons:
                    button.check_event(event)

            pygame.display.update()
            self.tick()

            if self.player:
                b2.disabled = False
                b2.value = f"Graj jako {self.player.name}"
                b2.render_text()

            if self.player != previous_player:
                for i, button in enumerate(buttons, 1):
                    rect_dims = (
                        button.rect.left,
                        button.rect.top,
                        self.menu_button_width,
                        button.rect.height,
                    )
                    new_rect = pygame.Rect(rect_dims)
                    button.rect = new_rect
                    button.rect.center = (
                        screen_width / 2,
                        i / (len(buttons) + 1) * screen_height,
                    )
                    previous_player = self.player

    def tick(self):
        self.clock.tick(self.FPS)

    def update(self):
        pass
