import pygame


def split_text_by_length(text, line_length=21):
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) <= line_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())

    return [line.strip() for line in lines]


class Answer:
    rect_dims = (0, 0, 420, 100)

    def __init__(self, text):
        self.rect = pygame.Rect(self.rect_dims)
        self.text = text
        self.highlighted = False
        self.highlight_color = None
        self.render_text()

    def highlight(self, color="GREEN"):
        self.highlighted = True
        self.highlight_color = color

    def unhighlight(self):
        self.highlighted = False
        self.highlight_color = None

    def render_text(self):
        from common.components.core.app import App

        app = App()
        font_name = app.theme.font_name
        font_size = 20
        font = pygame.font.Font(font_name, font_size)
        texts = split_text_by_length(self.text)
        texts = [font.render(text, True, app.theme.primary_color) for text in texts]
        self._texts = texts

    def update(self, surface):
        from common.components.core.app import App

        app = App()
        texts = self._texts

        if self.highlighted:
            surface.fill(self.highlight_color, self.rect)
            inflate_value = -8
            surface.fill(
                app.theme.secondary_color,
                self.rect.inflate(inflate_value, inflate_value),
            )
        else:
            surface.fill(app.theme.secondary_color, self.rect)

        pos = [0]
        if len(texts) == 1:
            pos = [-1 / 2]
        elif len(texts) == 2:
            pos = [-1, 0]
        elif len(texts) == 3:
            pos = [-3 / 2, -1 / 2, 1 / 2]
        elif len(texts) == 4:
            pos = [-2, -1, 0, 1]

        for i, text in zip(pos, texts):
            text_rect = text.get_rect(center=self.rect.center)
            text_rect.top = self.rect.center[1] + text_rect.height * i
            surface.blit(text, text_rect)
