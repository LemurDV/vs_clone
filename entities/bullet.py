import pygame

from entities.entity import Entity
from settings import ORANGE


class Bullet(Entity):
    def __init__(self, x, y, target, damage):
        super().__init__(x, y, 5, 5, ORANGE)
        self.target = target  # враг, в которого летит пуля
        self.damage = damage
        self.speed = 7

    def update(self, game):
        # Движение к цели, если цель активна
        if self.target and self.target.active:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            distance = max(0.1, (dx**2 + dy**2) ** 0.5)
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            self.move(dx, dy)

            # Проверка столкновения с целью
            if self.check_collision(self.target):
                self.target.take_damage(self.damage)
                self.destroy()
        else:
            # Если цель не активна, ищем новую ближайшую цель
            new_target = None
            min_distance = float("inf")
            for enemy in game.enemies:
                if enemy.active:
                    dist = self.distance_to(enemy)
                    if dist < min_distance:
                        min_distance = dist
                        new_target = enemy
            if new_target:
                self.target = new_target
            else:
                # Если врагов нет, уничтожаем пулю
                self.destroy()

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, self.rect.center, self.rect.width // 2
        )
