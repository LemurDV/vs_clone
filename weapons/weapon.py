from abc import ABC, abstractmethod

from settings import *


class Weapon(ABC):
    """Абстрактный базовый класс оружия"""

    def __init__(self, name, damage, cooldown):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown  # ms
        self.last_attack_time = 0
        self.owner = None
        self.level = 1
        self.max_level = 5

    @abstractmethod
    def update(self, game):
        """Обновление оружия"""
        pass

    @abstractmethod
    def draw(self, screen):
        """Отрисовка оружия"""
        pass

    def can_attack(self):
        """Проверка возможности атаки"""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_attack_time > self.cooldown

    def level_up(self):
        """Улучшение оружия"""
        if self.level < self.max_level:
            self.level += 1
            self.damage *= 1.5
            self.cooldown = max(100, self.cooldown * 0.9)
            return True
        return False
