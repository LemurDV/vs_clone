import pygame

from elements.base_element import BaseElement


class BloodElement(BaseElement):
    def __init__(self):
        super().__init__(
            name="blood",
            name_ui="Кровь",
            description="Увеличивает вампиризм",
            image_path="assets/elements/blood.png",
        )

    def apply(self, player):
        pass
