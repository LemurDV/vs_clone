import pygame

from elements.base_element import BaseElement


class BloodElement(BaseElement):
    def __init__(self):
        super().__init__(
            name="Кровь",
            description="Увеличивает вампиризм",
        )
        self.image = None
        self.load_image()

    def load_image(self):
        self.image = pygame.image.load(
            "assets/elements/blood.png"
        ).convert_alpha()
        # Масштабируйте до нужного размера, например 32x32
        self.image = pygame.transform.scale(self.image, (32, 32))

    def apply(self, player):
        pass
