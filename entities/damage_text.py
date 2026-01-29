import pygame

from entities.popup_text import PopupText
from settings import RED, WHITE, YELLOW


class DamageText(PopupText):
    def __init__(self, x, y, damage, color=RED, is_critical=False):
        super().__init__(
            x=x,
            y=y,
            text=damage,
            color=color,
            is_critical=is_critical,
        )
