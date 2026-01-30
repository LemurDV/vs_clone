import math

import pygame

from settings import ORANGE


class Projectile:
    """Класс летающего объекта"""

    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 15, 15)
        self.target = target
        self.damage = damage
        self.speed = 7
        self.radius = 4
        self.color = ORANGE
        self.active = True
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 3000  # 3 секунды

    def update(self):
        """Обновление пули"""
        if not self.active or not self.target.active:
            self.active = False
            return

        # Расчет направления к цели
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            # Нормализация и движение
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self, screen):
        """Отрисовка пули"""
        if self.active:
            pygame.draw.circle(
                screen, self.color, (int(self.x), int(self.y)), self.radius
            )

    def distance_to_target(self):
        """Расстояние до цели"""
        if not self.target.active:
            return float("inf")
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        return math.sqrt(dx**2 + dy**2)
