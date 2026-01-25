import math

from settings import ORANGE, pygame


class Projectile:
    """Класс летающего объекта"""

    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 7
        self.radius = 4
        self.color = ORANGE
        self.active = True
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 3000  # 3 секунды

    def update(self, game):
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

            # Проверка попадания
            bullet_rect = pygame.Rect(
                self.x - self.radius,
                self.y - self.radius,
                self.radius * 2,
                self.radius * 2,
            )
            if bullet_rect.colliderect(self.target.rect):
                # Добавляем шанс крита
                import random

                is_critical = random.random() < 0.1
                damage = self.damage * 2 if is_critical else self.damage

                if self.target.take_damage(damage, game, is_critical):
                    # Опыт уже создан в take_damage
                    pass
                self.active = False

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
