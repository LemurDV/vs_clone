import math

import pygame

from settings import ORANGE


class Projectile:
    """Класс летающего объекта"""

    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 7
        self.radius = 7
        self.color = ORANGE
        self.active = True

        # Прямоугольник для столкновений
        self.rect = pygame.Rect(x - 7, y - 7, 14, 14)

    def update(self):
        """Двигаемся к цели"""
        if not self.active or not self.target.active:
            self.active = False
            return

        # Двигаемся к цели
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y

        # Если цель очень близко - попадание
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < self.speed:
            self.x = self.target.rect.centerx
            self.y = self.target.rect.centery
        else:
            # Плавное движение
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

        # Обновляем прямоугольник
        self.rect.center = (int(self.x), int(self.y))

    def is_collision(self):
        """Проверяем, попали ли в цель"""
        if not self.active or not self.target.active:
            return False

        # Простая проверка расстояния
        distance = math.sqrt(
            (self.x - self.target.rect.centerx) ** 2
            + (self.y - self.target.rect.centery) ** 2
        )

        # Попали, если близко к цели
        return distance < max(self.radius, self.target.rect.width // 2)

    def draw(self, screen):
        """Рисуем пулю"""
        if self.active:
            pygame.draw.circle(
                screen, self.color, (int(self.x), int(self.y)), self.radius
            )

            glow_color = (
                min(255, self.color[0] + 100),
                min(255, self.color[1] + 100),
                min(255, self.color[2] + 100),
            )
            pygame.draw.circle(
                screen, glow_color, (int(self.x), int(self.y)), self.radius // 2
            )
