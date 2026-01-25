from abc import ABC, abstractmethod


class Upgrade(ABC):
    """Абстрактный базовый класс улучшения"""

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def apply(self, player):
        """Применение улучшения к игроку"""
        pass
