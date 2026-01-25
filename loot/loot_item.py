# loot/loot_item.py
from abc import ABC, abstractmethod

import pygame


class LootItem(ABC):
    def __init__(self, x, y, width=20, height=20):
        self.rect = pygame.Rect(x, y, width, height)
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
        player = game.player
        if player and player.active:
            distance = self.distance_to(player)

            if distance < player.magnet_radius:
                # Движение к игроку
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery

                if distance > 0:
                    dx = (dx / distance) * self.speed
                    dy = (dy / distance) * self.speed
                    self.move(dx, dy)

            # Проверка сбора
            if self.rect.colliderect(player.rect):
                self.apply(player)
                self.active = False
