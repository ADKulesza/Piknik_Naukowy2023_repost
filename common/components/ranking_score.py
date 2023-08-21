from pathlib import Path

import pygame

from common.themes.utils import currnet_theme


class Score:
    def __init__(self, rect, data, **kwargs):
        self.rect = pygame.Rect(rect)
        self.data = data
        self._text = None

        self.process_kwargs(kwargs)

        self.ready = False

    def process_kwargs(self, kwargs):
        """Various optional customization you can change by passing kwargs."""
        theme = currnet_theme()

        settings = {
            "color": theme.secondary_color,
            "font": pygame.font.Font(theme.font_name, theme.font_size),
            "font_color": theme.primary_color,
            "odd": False,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Score has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        """Pre render the button text."""
        text = f"        {self.data.get('name'):^15}  {self.data.get('score'):^5}"
        text = self.font.render(text, True, self.font_color)
        self._text = text

    def check_event(self, event):
        pass

    def prepare(self):
        position = self.data.get("position")
        if position in (1, 2, 3):
            if position == 1:
                pos_img = pygame.image.load(
                    Path(__file__).parent / "static/pos1.png"
                ).convert_alpha()
            elif position == 2:
                pos_img = pygame.image.load(
                    Path(__file__).parent / "static/pos2.png"
                ).convert_alpha()
            elif position == 3:
                pos_img = pygame.image.load(
                    Path(__file__).parent / "static/pos3.png"
                ).convert_alpha()
        else:
            pos_img = self.font.render(str(position), True, self.font_color)
        self.pos = pos_img

        self.render_text()
        self.ready = True

    def update(self, surface):
        # for entity in self.sprite:
        #     import  ipdb; ipdb.set_trace()
        #     entity.rect.center = self.rect.center

        if not self.ready:
            self.prepare()

        color = self.color
        text = self._text
        surface.fill(pygame.Color("black"), self.rect)
        surface.fill(color, self.rect.inflate(-4, -4))

        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

        pos_rect = self.pos.get_rect()
        pos_rect.center = (self.rect.x + 80, self.rect.y + self.rect.height / 2)

        surface.blit(self.pos, pos_rect)


class ScoreHeader:
    def __init__(self, rect, data="Wyniki", **kwargs):
        self.rect = pygame.Rect(rect)
        self.data = data
        self.value = data
        self._text = None

        self.process_kwargs(kwargs)
        self.render_text()

    def process_kwargs(self, kwargs):
        """Various optional customization you can change by passing kwargs."""
        theme = currnet_theme()

        settings = {
            "color": theme.secondary_color,
            "font": pygame.font.Font(theme.font_name, theme.font_size),
            "font_color": theme.primary_color,
            "odd": False,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Score has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        """Pre render the button text."""
        if self.value:
            self._text = self.font.render(self.value, True, self.font_color)

    def update(self, surface):
        if self._text:
            color = self.color
            text = self._text
            surface.fill(pygame.Color("black"), self.rect)
            surface.fill(color, self.rect.inflate(-4, -4))

            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def check_event(self, event):
        pass
