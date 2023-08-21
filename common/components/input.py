import string

import pygame

from common.themes.utils import currnet_theme

# class TextInputBox(pygame.sprite.Sprite):
#     def __init__(self, x, y, w, font):
#         super().__init__()
#         self.color = currnet_theme().primary_color
#         self.backcolor = currnet_theme().secondary_color
#         self.pos = (x, y)
#         self.width = w
#
#         self.active = True
#         self.text = ""
#
#         self.image = None
#         self.rect = None
#
#         self.render_text()
#
#     def render_text(self):
#         t_surf = self.font.render(self.text, True, self.backcolor, self.color)
#         self.image = pygame.Surface(
#             (max(self.width, t_surf.get_width() + 10), t_surf.get_height() + 10),
#             pygame.SRCALPHA,
#         )
#         if self.backcolor:
#             self.image.fill(self.backcolor)
#         self.image.blit(t_surf, (5, 5))
#         pygame.draw.rect(
#             self.image, self.backcolor, self.image.get_rect().inflate(-2, -2), 2
#         )
#         self.rect = self.image.get_rect(topleft=self.pos)
#
#     def update(self, event_list):
#         for event in event_list:
#             if event.type == pygame.KEYDOWN and self.active:
#                 if event.key == pygame.K_RETURN:
#                     self.active = False
#                 elif event.key == pygame.K_BACKSPACE:
#                     self.text = self.text[:-1]
#                 else:
#                     if event.unicode == "\x1b":
#                         continue
#                     self.text += event.unicode
#                 self.render_text()


class TextInputBox:
    def __init__(self, x, y, w, font, prefix="Podaj imię: "):
        self.x = x
        self.y = y
        self.font = font
        self.prefix = prefix
        self.text_color = currnet_theme().secondary_color
        self.value = ""
        self.done = False

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif event.key == pygame.K_RETURN:
                self.done = True
            elif event.key == pygame.K_KP_ENTER:
                self.done = True
            elif event.unicode:
                if event.unicode in string.printable:
                    self.value += event.unicode

    def update(self, surface):
        text_surface = self.font.render(self.prefix + self.value, True, self.text_color)
        rect = text_surface.get_rect()
        rect.center = self.x, self.y
        surface.blit(text_surface, rect)
