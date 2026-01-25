from abc import ABC, abstractmethod

import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Entity(ABC):
    """Абстрактный базовый класс для всех игровых сущностей"""

    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.radius = 10
        self.color = color
        self.speed = 0
        self.active = True
        self.creation_time = pygame.time.get_ticks()

    @abstractmethod
    def update(self, game):
        """Обновление состояния сущности"""
        pass

    @abstractmethod
    def draw(self, screen):
        """Отрисовка сущности"""
        pass

    def move(self, dx, dy):
        """Перемещение сущности"""
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(
            self.radius, min(SCREEN_WIDTH - self.radius, self.rect.x)
        )
        self.rect.y = max(
            self.radius, min(SCREEN_HEIGHT - self.radius, self.rect.y)
        )

    def distance_to(self, other_entity):
        """Расстояние до другой сущности"""
        return (
            (self.rect.centerx - other_entity.rect.centerx) ** 2
            + (self.rect.centery - other_entity.rect.centery) ** 2
        ) ** 0.5

    def check_collision(self, other_entity):
        if hasattr(self, "radius") and hasattr(other_entity, "radius"):
            # Круг-круг
            return self.distance_to(other_entity) <= (
                self.radius + other_entity.radius
            )
        elif hasattr(self, "radius") or hasattr(other_entity, "radius"):
            # Круг-прямоугольник
            circle = self if hasattr(self, "radius") else other_entity
            rect = other_entity.rect if hasattr(self, "radius") else self.rect
            return self.circle_rect_collision(circle, rect)
        else:
            # Прямоугольник-прямоугольник
            return self.rect.colliderect(other_entity.rect)

    def circle_rect_collision(self, circle, rect):
        """Проверка столкновения круга с прямоугольником"""
        # Находим ближайшую к кругу точку прямоугольника
        closest_x = max(rect.left, min(circle.rect.centerx, rect.right))
        closest_y = max(rect.top, min(circle.rect.centery, rect.bottom))

        # Проверяем расстояние от центра круга до этой точки
        distance_x = circle.rect.centerx - closest_x
        distance_y = circle.rect.centery - closest_y

        return (distance_x**2 + distance_y**2) <= (circle.radius**2)

    def destroy(self):
        """Уничтожение сущности"""
        self.active = False
