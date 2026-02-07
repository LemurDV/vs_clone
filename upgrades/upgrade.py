from abc import ABC, abstractmethod

import pygame


class Upgrade(ABC):
    """Абстрактный базовый класс улучшения"""

    def __init__(self, name, description, image_path=None):
        self.name = name
        self.description = description
        self.image_path = image_path
        self.image = None
        self.load_image()

    def load_image(self):
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

    @abstractmethod
    def apply(self, player):
        """Применение улучшения к игроку"""
        pass
