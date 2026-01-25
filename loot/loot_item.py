# loot/loot_item.py
from abc import ABC, abstractmethod

import pygame


class LootItem(ABC):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.lifetime = 10000  # 10 секунд
        self.creation_time = pygame.time.get_ticks()
        self.active = True
        self.magnet_radius = 80  # Радиус притяжения к игроку

    @abstractmethod
    def apply(self, player):
        """Применение лута к игроку"""
        pass

    @abstractmethod
    def draw(self, screen):
        """Отрисовка лута"""
        pass

    def update(self, game):
        """Обновление лута"""
        current_time = pygame.time.get_ticks()

        # Уничтожение по времени
        if current_time - self.creation_time > self.lifetime:
            self.active = False
            return

        # Притягивание к игроку
        player = game.player
        if player and player.active:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = (dx**2 + dy**2) ** 0.5

            if distance < self.magnet_radius:
                speed = 4 if distance > 20 else 0
                if distance > 0:
                    self.rect.x += (dx / distance) * speed
                    self.rect.y += (dy / distance) * speed

            # Проверка сбора
            if self.rect.colliderect(player.rect):
                self.apply(player)
                self.active = False
