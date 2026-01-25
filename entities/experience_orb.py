from entities.entity import Entity
from settings import *


class ExperienceOrb(Entity):
    """Сфера опыта"""

    def __init__(self, x, y, value):
        super().__init__(x, y, 8, 8, YELLOW)
        self.value = value
        self.magnet_radius = 100  # Радиус притягивания к игроку

    def update(self, game):
        """Обновление сферы опыта"""
        player = game.player
        if player and player.active:
            distance = self.distance_to(player)

            if distance < self.magnet_radius:
                # Движение к игроку
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery

                if distance > 0:
                    speed = 5
                    dx = (dx / distance) * speed
                    dy = (dy / distance) * speed
                    self.move(dx, dy)

            # Проверка сбора
            if self.check_collision(player):
                player.add_experience(self.value)
                self.destroy()

    def draw(self, screen):
        """Отрисовка сферы опыта"""
        pygame.draw.circle(
            screen, self.color, self.rect.center, self.rect.width // 2
        )
