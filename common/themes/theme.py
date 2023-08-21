from pathlib import Path

from common.themes.utils import get_theme


class Theme:
    def __init__(self, file_name):
        theme = get_theme(file_name)
        for key, value in theme.items():
            if key == "font_name":
                value = Path(__file__).parent / value

            setattr(self, key, value)


# from types import SimpleNamespace
#
#
# def assign(target, *args, suffix):
#     ls = target
#     for i in range(len(args) - 1):
#         a = args[i]
#         ns = SimpleNamespace()
#         setattr(ls, a, ns)
#         ls = ns
#     setattr(ls, args[-1], suffix)
#     return ls
#
#
# a = SimpleNamespace()
# assign(a, 'a', 'b', 'c', suffix={'name': 'james'})
# print(a.a.b.c)
# # {'name': 'james'}
