import math

from loguru import logger
import pygame

from config import WHITE
from weapons.weapon import Weapon


class AuraWeapon(Weapon):
    def __init__(self, name, damage, radius, owner, color=(150, 50, 200)):
        super().__init__(name, damage, 500, owner)  # Кулдаун 500 мс
        self.radius = radius
        self.color = color
        self.active = True
        self.base_radius = radius  # Сохраняем базовый радиус

    def update(self, current_time, enemies):
        """Постоянно наносит урон врагам в радиусе с кулдауном"""
        if not self.active:
            return

        if current_time - self.last_attack < self.cooldown:
            return

        enemies_hit = False
        for enemy in enemies[:]:
            dx = enemy.x - self.owner.x
            dy = enemy.y - self.owner.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < self.radius + enemy.radius:
                alive, damage_dealt = enemy.take_damage(self.damage)
                enemies_hit = True

        if enemies_hit:
            self.last_attack = current_time

    def draw(self, screen):
        """Рисуем ауру вокруг игрока"""
        if not self.active:
            return

        # Прозрачная аура
        aura_surface = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA
        )
        alpha = 50  # Прозрачность
        pygame.draw.circle(
            aura_surface,
            (*self.color, alpha),
            (self.radius, self.radius),
            self.radius,
        )

        screen.blit(
            aura_surface,
            (int(self.owner.x - self.radius), int(self.owner.y - self.radius)),
        )

        # Контур ауры
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.owner.x), int(self.owner.y)),
            self.radius,
            2,
        )

        # level_text = font.render(f"Lvl {self.level}", True, WHITE)
        # screen.blit(
        #     level_text,
        #     (int(self.owner.x - level_text.get_width() // 2),
        #      int(self.owner.y - self.radius - 20))
        # )

    def level_up(self, player_dmg):
        """Улучшение ауры"""
        # if super().level_up():
        # Дополнительные бонусы для ауры при улучшении
        self.radius = self.base_radius + (self.level - 1) * 10
        # Уменьшаем кулдаун
        # self.cooldown = max(200, self.cooldown - 50)
        self.level += 1
        logger.info(
            f"Аура улучшена! {self.level=}, {self.radius=}, {self.damage=}, {self.cooldown=}"
        )
        return True
        # return False
