import os
from pathlib import Path


class SelectAvatar:
    AVATAR_CHOICE = {
        "Ada Lovelace": "lovelace",
        "Albert Einstein": "einstein",
        "Mikołaj Kopernik": "kopernik",
        "Maria Skłodowska": "sklodowska",
    }

    def __init__(self):
        self.avatar = None
        self.av_path = Path(__file__).parent / "static/avatars"

    def set_avatar(self, av_name):
        self.avatar = av_name

    @property
    def avatar_choices(self):
        return self.AVATAR_CHOICE

    def get_avatar_path(self, av_name):
        """
        Use only in select avatar menu
        """
        av_path = os.path.join(
            self.av_path,
            self.AVATAR_CHOICE[av_name],
            self.AVATAR_CHOICE[av_name] + ".png",
        )

        return av_path

    def get_dir_path(self):
        av_path = os.path.join(self.av_path, self.AVATAR_CHOICE[self.avatar])

        return av_path

    def get_sztanga_paths(self):
        LOW_POINT = "_sztanga_nisko.png"
        HIGH_POINT = "_sztanga_wysoko.png"
        av_path = os.path.join(self.av_path, self.AVATAR_CHOICE[self.avatar])

        anim_paths = [
            os.path.join(av_path, self.AVATAR_CHOICE[self.avatar] + LOW_POINT),
            os.path.join(av_path, self.AVATAR_CHOICE[self.avatar] + HIGH_POINT),
        ]

        return anim_paths

    def get_ufo_paths(self):
        PATH = "_ufo.png"
        av_path = os.path.join(self.av_path, self.AVATAR_CHOICE[self.avatar])

        anim_paths = [os.path.join(av_path, self.AVATAR_CHOICE[self.avatar] + PATH)]

        return anim_paths
