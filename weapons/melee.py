# melee_weapon.py
import math

import pygame

from weapons.weapon import Weapon


class MeleeWeapon(Weapon):
    def __init__(self, name, damage, radius, owner, color=(255, 150, 50)):
        super().__init__(name, damage, 3000, owner)  # 3 секунды кулдаун
        self.radius = radius
        self.color = color
        self.attack_active = False
        self.attack_duration = 300  # 0.3 секунды длится атака
        self.attack_start_time = 0

    def update(self, current_time, enemies):
        """Периодическая атака по области"""
        if current_time - self.last_attack > self.cooldown:
            self.attack_active = True
            self.attack_start_time = current_time
            self.last_attack = current_time

            # Наносим урон всем врагам в радиусе
            for enemy in enemies[:]:
                dx = enemy.x - self.owner.x
                dy = enemy.y - self.owner.y
                distance = math.sqrt(dx * dx + dy * dy)

                if distance < self.radius + enemy.radius:
                    enemy.take_damage(self.damage * self.level)

        # Выключаем атаку после длительности
        if (
            self.attack_active
            and current_time - self.attack_start_time > self.attack_duration
        ):
            self.attack_active = False

    def draw(self, screen):
        """Рисуем взрывную волну при атаке"""
        if self.attack_active:
            # Рисуем расширяющийся круг
            progress = min(
                1.0,
                (pygame.time.get_ticks() - self.attack_start_time)
                / self.attack_duration,
            )
            current_radius = int(self.radius * progress)

            # Полупрозрачный круг
            aura_surface = pygame.Surface(
                (current_radius * 2, current_radius * 2), pygame.SRCALPHA
            )
            alpha = 100 - int(progress * 70)  # Исчезает
            pygame.draw.circle(
                aura_surface,
                (*self.color, alpha),
                (current_radius, current_radius),
                current_radius,
            )

            screen.blit(
                aura_surface,
                (self.owner.x - current_radius, self.owner.y - current_radius),
            )
