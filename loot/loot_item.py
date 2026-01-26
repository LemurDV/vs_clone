from abc import ABC, abstractmethod

import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class LootItem(ABC):
    def __init__(self, x, y, width=20, height=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.creation_time = pygame.time.get_ticks()
        self.active = True
        self.magnet_radius = 80  # Радиус притяжения к игроку
        self.speed = 5

    @abstractmethod
    def apply(self, player):
        """Применение лута к игроку"""
        pass

    @abstractmethod
    def draw(self, screen):
        """Отрисовка лута"""
        pass

    def distance_to(self, other_entity):
        """Расстояние до другой сущности"""
        return (
            (self.rect.centerx - other_entity.rect.centerx) ** 2
            + (self.rect.centery - other_entity.rect.centery) ** 2
        ) ** 0.5

    def move(self, dx, dy):
        """Перемещение сущности"""
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(
            self.rect.width, min(SCREEN_WIDTH - self.rect.width, self.rect.x)
        )
        self.rect.y = max(
            self.rect.width, min(SCREEN_HEIGHT - self.rect.width, self.rect.y)
        )

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
