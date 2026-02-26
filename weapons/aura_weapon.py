import pygame

from settings import (
    AURA_MULTIPLIER_DAMAGE,
    AURA_MULTIPLIER_RADIUS,
    PURPLE,
)
from weapons.weapon import Weapon, WeaponTypes


class AuraWeapon(Weapon):
    def __init__(
        self,
        name="aura",
        name_ui="Аура",
        damage=2,
        cooldown=800,
        weapon_type=WeaponTypes.AURA,
        causes_bleeding_chance: float = 0.0,
        causes_burn_chance: float = 0.0,
        causes_poison_chance: float = 0.0,
    ):
        super().__init__(
            name=name,
            name_ui=name_ui,
            damage=damage,
            cooldown=cooldown,
            weapon_type=weapon_type,
            causes_bleeding_chance=causes_bleeding_chance,
            causes_burn_chance=causes_burn_chance,
            causes_poison_chance=causes_poison_chance,
        )
        self.radius = 50
        self.color = PURPLE

    def update(self, game):
        pass

    def can_attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.cooldown:
            self.last_attack_time = pygame.time.get_ticks()
            return True
        return False

    def is_collision(self, enemy) -> bool:
        if enemy.active and self.owner.distance_to(enemy) <= self.radius:
            return True
        return False

    def get_damage(self):
        return self.damage + self.owner.get_damage() // 2

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
