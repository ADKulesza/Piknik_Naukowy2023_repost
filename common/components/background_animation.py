from common.components.animation import Animation


class BackgroundAnimation(Animation):
    def __init__(self, path):
        from common.components.core.app import App

        app = App()
        super().__init__(path=path, dimensions=app.canvas.get_size())
