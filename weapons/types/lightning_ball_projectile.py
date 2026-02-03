import math
import random

import pygame

from settings import BLUE
from weapons.types.projectile import Projectile


class LightningBallProjectile(Projectile):
    """Кастомный класс шара молнии"""

    def __init__(self, x, y, target, damage):
        super().__init__(x, y, target, damage)
        self.color = BLUE
        self.radius = 10  # Больше обычной пули
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20)
        self.pulse_time = 0  # Для пульсации

    def draw(self, screen):
        """Рисуем шар молнии с эффектом пульсации"""
        if not self.active:
            return

        self.pulse_time += 1

        # Пульсирующий радиус
        pulse_radius = self.radius + math.sin(self.pulse_time * 0.2) * 2

        # Основной шар
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), int(pulse_radius)
        )

        # Внутреннее свечение
        inner_color = (
            min(255, self.color[0] + 100),
            min(255, self.color[1] + 100),
            min(255, self.color[2] + 100),
        )
        pygame.draw.circle(
            screen,
            inner_color,
            (int(self.x), int(self.y)),
            int(pulse_radius * 0.6),
        )

        # Электрические искры (случайные точки вокруг)
        for _ in range(5):
            angle = random.random() * math.pi * 2
            distance = pulse_radius + random.randint(2, 8)
            spark_x = self.x + math.cos(angle) * distance
            spark_y = self.y + math.sin(angle) * distance

            pygame.draw.circle(
                screen, (255, 255, 200), (int(spark_x), int(spark_y)), 1
            )
