from pathlib import Path

import yaml


def parse_theme(theme):
    return theme


def get_theme(file_name):
    path = Path(file_name)
    if not path.exists():
        raise ValueError(f"There is no theme for {file_name}")

    with open(path) as f:
        theme = yaml.safe_load(f)

    parse_theme(theme)
    return theme


def currnet_theme():
    from common.components.core.app import App

    return App().theme
