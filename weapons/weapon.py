from abc import ABC, abstractmethod

import pygame


class Weapon(ABC):
    """Абстрактный базовый класс оружия"""

    def __init__(self, name, name_ui, damage, cooldown, weapon_type):
        self.name = name
        self.name_ui = name_ui
        self.damage = damage
        self.cooldown = cooldown  # ms
        self.last_attack_time = 0
        self.owner = None
        self.level = 1
        self.max_level = 5
        self.weapon_type = weapon_type

    @abstractmethod
    def update(self, game):
        """Обновление оружия"""
        pass

    def is_collision(self, enemy) -> bool:
        pass

    def action_after_deal_damage(self):
        self.last_attack_time = pygame.time.get_ticks()

    def get_damage(self):
        return self.damage + self.owner.get_damage() // 2

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
