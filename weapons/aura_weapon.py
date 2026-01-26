import random

from settings import (
    AURA_MULTIPLIER_DAMAGE,
    AURA_MULTIPLIER_RADIUS,
    PURPLE,
    pygame,
)
from weapons.weapon import Weapon


class AuraWeapon(Weapon):
    """Оружие - аура вокруг игрока"""

    def __init__(self):
        super().__init__("aura", "Аура", 5, 500)
        self.radius = 50
        self.color = PURPLE

    def update(self, game):
        """Обновление ауры"""
        if not self.owner or not self.owner.active:
            return

        if self.can_attack():
            self.attack(game)
            self.last_attack_time = pygame.time.get_ticks()

    def attack(self, game):
        """Атака врагов в радиусе"""
        owner_damage = (
            self.owner.get_damage() if hasattr(self.owner, "get_damage") else 1
        )
        total_damage = self.damage * owner_damage

        is_critical = random.random() < 0.1
        if is_critical:
            total_damage *= 2

        for enemy in game.enemy_manager.enemies[:]:
            if enemy.active and self.owner.distance_to(enemy) <= self.radius:
                if enemy.take_damage(total_damage, game, is_critical):
                    pass

    def draw(self, screen):
        """Отрисовка ауры"""
        if self.owner and self.owner.active:
            # Прозрачная аура
            aura_surface = pygame.Surface(
                (self.radius * 2, self.radius * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                aura_surface,
                (*self.color, 100),
                (self.radius, self.radius),
                self.radius,
            )
            screen.blit(
                aura_surface,
                (
                    self.owner.rect.centerx - self.radius,
                    self.owner.rect.centery - self.radius,
                ),
            )

    def level_up(self):
        """Улучшение оружия"""
        self.level += 1
        self.increase_damage()
        self.increase_radius()
        return True

    def increase_damage(self):
        self.damage += AURA_MULTIPLIER_DAMAGE

    def increase_radius(self):
        self.radius += AURA_MULTIPLIER_RADIUS
