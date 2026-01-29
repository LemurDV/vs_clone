from entities.popup_text import PopupText
from settings import BLACK, GREEN


class HealText(PopupText):
    def __init__(self, x, y, heal, color=GREEN, is_critical=False):
        super().__init__(
            x=x,
            y=y,
            text=f"+{heal}",
            color=color,
            is_critical=is_critical,
        )
