from abc import ABC, abstractmethod

import pygame


class BaseElement(ABC):
    def __init__(self, name, description, image_path=None):
        self.name = name
        self.description = description
        self.image_path = image_path
        self.image = None
        self.load_image()

    def load_image(self):
        self.image = pygame.image.load(
            "assets/elements/blood.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

    @abstractmethod
    def apply(self, player):
        pass
