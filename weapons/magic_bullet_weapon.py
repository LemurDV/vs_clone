import math

import pygame

from settings import *
from weapons.weapon import Weapon


class MagicBullet:
    """Класс магической пули"""

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
                if self.target.take_damage(self.damage):
                    # Враг убит - создаем сферу опыта
                    game.spawn_experience_orb(
                        self.target.rect.centerx,
                        self.target.rect.centery,
                        self.target.experience_value,
                    )
                self.active = False

        # Уничтожение по истечении времени жизни
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
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


class MagicBulletWeapon(Weapon):
    """Оружие - магические пули, летящие к ближайшим врагам"""

    def __init__(self):
        super().__init__("Магическая пуля", 3, 1000)
        self.bullets = []
        self.max_bullets = 1
        self.bullet_speed = 6
        self.upgrade_levels = [
            {"max_bullets": 2, "damage": 4, "cooldown": 800},
            {"max_bullets": 3, "damage": 5, "cooldown": 700},
            {"max_bullets": 4, "damage": 6, "cooldown": 600},
        ]

    def update(self, game):
        """Обновление оружия"""
        # Обновление существующих пуль
        for bullet in self.bullets[:]:
            if bullet.active:
                bullet.update(game)
            else:
                self.bullets.remove(bullet)

        # Стрельба
        if self.can_attack() and self.owner and self.owner.active:
            self.shoot(game)

    def shoot(self, game):
        """Выстрел пулями"""
        # Ищем активных врагов
        active_enemies = [e for e in game.enemies if e.active]

        if not active_enemies:
            return

        # Определяем, сколько пуль можем выпустить
        bullets_to_shoot = min(
            self.max_bullets - len(self.bullets), len(active_enemies)
        )

        if bullets_to_shoot <= 0:
            return

        # Выбираем ближайших врагов
        enemies_by_distance = sorted(
            active_enemies, key=lambda e: self.owner.distance_to(e)
        )

        for i in range(bullets_to_shoot):
            if i < len(enemies_by_distance):
                target = enemies_by_distance[i]
                owner_damage = (
                    self.owner.get_damage()
                    if hasattr(self.owner, "get_damage")
                    else 1
                )
                total_damage = self.damage * owner_damage

                bullet = MagicBullet(
                    self.owner.rect.centerx,
                    self.owner.rect.centery,
                    target,
                    total_damage,
                )
                self.bullets.append(bullet)

        self.last_attack_time = pygame.time.get_ticks()

    def draw(self, screen):
        """Отрисовка пуль"""
        for bullet in self.bullets:
            bullet.draw(screen)

    def level_up(self):
        """Улучшение оружия"""
        if self.level < self.max_level:
            self.level += 1
            level_info = self.upgrade_levels[self.level - 1]
            self.max_bullets = level_info["max_bullets"]
            self.damage = level_info["damage"]
            self.cooldown = level_info["cooldown"]
            return True
        return False

    @property
    def is_weapon(self):
        """Является ли улучшением-оружием"""
        return True
