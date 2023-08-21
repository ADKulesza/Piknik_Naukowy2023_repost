import sys

import pygame

from common.themes.utils import currnet_theme


def exit():
    from common.components.core.app import App

    app = App()
    app.amplifier.destroy()
    pygame.quit()
    sys.exit()


class Button:
    """A fairly straight forward button class."""

    def __init__(self, rect, function, **kwargs):
        self.rect = pygame.Rect(rect)
        self.function = function

        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self._cursor = None
        self.process_kwargs(kwargs)
        self._text = None
        self.render_text()

    def process_kwargs(self, kwargs):
        """Various optional customization you can change by passing kwargs."""
        theme = currnet_theme()

        settings = {
            "value": None,
            "font": pygame.font.Font(theme.font_name, theme.font_size),
            "color": theme.secondary_color,
            "call_on_release": True,
            "hover_color": None,
            "clicked_color": None,
            "font_color": theme.primary_color,
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
            "disabled": False,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        """Pre render the button text."""
        if self.value:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.value, True, color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.value, True, color)
            self._text = self.font.render(self.value, True, self.font_color)

    def check_event(self, event):
        """The button needs to be passed events from your program event loop."""
        if self.disabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()

    def on_release(self, event):
        if self.clicked and self.call_on_release:
            self.function()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()

            if self.disabled:
                if not self._cursor:
                    self._cursor = pygame.mouse.get_cursor()
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            self.hovered = False
            if self._cursor:
                pygame.mouse.set_cursor(*self._cursor)
            self._cursor = None

    def update(self, surface):
        """Update needs to be called every frame in the main loop."""
        color = self.color
        text = self._text
        self.check_hover()
        if self.clicked and self.clicked_color:
            color = self.clicked_color
            if self.clicked_font_color:
                text = self.clicked_text
        elif self.hovered and self.hover_color:
            color = self.hover_color
            if self.hover_font_color:
                text = self.hover_text
        surface.fill(pygame.Color("black"), self.rect)
        surface.fill(color, self.rect.inflate(-4, -4))
        if self._text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)


class ExitButton(Button):
    def __init__(self, rect, value="Wyjście", **kwargs):
        function = self.exit
        kwargs["value"] = value
        super().__init__(rect, function=function, **kwargs)

    @staticmethod
    def exit():
        exit()


class AvatarChoiceButton(Button):
    def __init__(self, rect, function, **kwargs):
        kwargs["call_on_release"] = False
        super().__init__(rect, function=function, **kwargs)
        self.av_name = kwargs["value"]

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function(self.av_name)

    def on_release(self, event):
        if self.clicked and self.call_on_release:
            self.function(self.av_name)
        self.clicked = False
