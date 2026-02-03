import math

from loguru import logger
import pygame

from settings import (
    DARK_GREEN,
    GREEN,
    SCYTHE_MULTIPLIER_ANGLE,
    SCYTHE_MULTIPLIER_COOLDOWN,
    SCYTHE_MULTIPLIER_DAMAGE,
    SCYTHE_MULTIPLIER_RANGE,
    WHITE,
    YELLOW,
)
from weapons.weapon import Weapon


class ScytheWeapon(Weapon):
    """Оружие - коса, которая бьет в конусе в направлении ближайшего врага"""

    def __init__(self):
        super().__init__(
            name="scythe",
            name_ui="Смертельная коса",
            damage=5,
            cooldown=1200,
            weapon_type="melee",
        )

        # Параметры конуса атаки
        self.attack_range = 80
        self.attack_angle = 60
        self.attack_duration = 300
        self.attack_start_time = 0
        self.is_attacking = False

        # Направление атаки (в радианах)
        self.attack_direction = 0  # 0 = вправо

        # Для анимации (если захотим визуализировать без спрайта)
        self.attack_progress = 0  # 0..1

    def update(self, game):
        """Обновление состояния косы"""
        current_time = pygame.time.get_ticks()

        if self.is_attacking:
            self.attack_progress = min(
                1.0,
                (current_time - self.attack_start_time) / self.attack_duration,
            )

            if current_time - self.attack_start_time > self.attack_duration:
                self.is_attacking = False
                self.attack_progress = 0

    def shoot(self, enemies, game):
        """Атака косой в направлении ближайшего врага"""
        if self.is_attacking:
            return

        # Находим ближайшего активного врага для определения направления
        active_enemies = [e for e in enemies if e.active]
        if not active_enemies:
            return

        # Находим ближайшего врага
        nearest_enemy = min(
            active_enemies, key=lambda e: self.owner.distance_to(e)
        )

        # Вычисляем направление к ближайшему врагу
        dx = nearest_enemy.rect.centerx - self.owner.rect.centerx
        dy = nearest_enemy.rect.centery - self.owner.rect.centery

        # Сохраняем направление атаки (в радианах)
        self.attack_direction = math.atan2(dy, dx)

        # Запускаем атаку
        self.is_attacking = True
        self.attack_start_time = pygame.time.get_ticks()
        self.attack_progress = 0

        # Находим всех врагов в конусе в этом направлении
        hit_enemies = self.get_enemies_in_cone(enemies, self.attack_direction)
        self.hit_enemies = len(hit_enemies)

        if hit_enemies:
            total_damage = self.damage + self.owner.get_damage()
            for enemy in hit_enemies:
                enemy.take_damage(total_damage, game)

    def get_enemies_in_cone(self, enemies, direction):
        """Возвращает врагов, находящихся в конусе атаки в заданном направлении"""
        if not self.owner:
            return []

        hit_enemies = []
        player_pos = pygame.math.Vector2(self.owner.rect.center)

        # Преобразуем направление в вектор
        facing_vector = pygame.math.Vector2(
            math.cos(direction), math.sin(direction)
        )

        for enemy in enemies:
            if not enemy.active:
                continue

            enemy_pos = pygame.math.Vector2(enemy.rect.center)

            # Проверяем расстояние
            distance = player_pos.distance_to(enemy_pos)
            if distance > self.attack_range:
                continue

            # Проверяем угол
            if self.is_in_cone(player_pos, facing_vector, enemy_pos):
                hit_enemies.append(enemy)

        return hit_enemies

    def is_in_cone(self, player_pos, facing_vector, enemy_pos):
        """Проверяет, находится ли точка в конусе"""
        to_enemy = enemy_pos - player_pos

        if to_enemy.length() == 0:
            return True

        to_enemy_normalized = to_enemy.normalize()

        # Вычисляем угол между направлением атаки и направлением к врагу
        dot_product = facing_vector.dot(to_enemy_normalized)

        # Защита от ошибок округления
        dot_product = max(-1, min(1, dot_product))

        angle_rad = math.acos(dot_product)
        angle_deg = math.degrees(angle_rad)

        # Проверяем, вписывается ли угол в половину угла конуса
        return angle_deg <= (self.attack_angle / 2)

    def draw(self, screen):
        """Отрисовка области атаки (для дебага)"""
        if not self.is_attacking or not self.owner:
            return

        player_center = self.owner.rect.center

        # Только область атаки, без отрисовки косы
        self.draw_attack_cone(screen, player_center, self.attack_direction)

        # Простая индикация направления (если нужно)
        # self.draw_direction_indicator(
        #     screen, player_center, self.attack_direction
        # )

    def draw_attack_cone(self, screen, player_center, direction):
        # Полностью заполненный яркий конус
        half_angle = math.radians(self.attack_angle / 2)
        points = [player_center]
        for i in range(20):
            angle = direction - half_angle + (2 * half_angle * i / 20)
            x = player_center[0] + math.cos(angle) * self.attack_range
            y = player_center[1] + math.sin(angle) * self.attack_range
            points.append((x, y))

        # Яркий полупрозрачный конус
        s = pygame.Surface(
            (screen.get_width(), screen.get_height()), pygame.SRCALPHA
        )
        pygame.draw.polygon(s, (255, 0, 0, 100), points)  # Красный, 100 альфа
        screen.blit(s, (0, 0))

        # Текст с параметрами
        font = pygame.font.Font(None, 24)
        text = font.render(
            f"Range: {self.attack_range}  Angle: {self.attack_angle}°",
            True,
            WHITE,
        )
        screen.blit(text, (player_center[0] - 100, player_center[1] - 40))

    def draw_direction_indicator(self, screen, player_center, direction):
        """Простая индикация направления атаки"""
        # Маленький круг на конце направления
        end_x = player_center[0] + math.cos(direction) * self.attack_range * 0.8
        end_y = player_center[1] + math.sin(direction) * self.attack_range * 0.8

        # Рисуем пульсирующий круг
        pulse_size = 5 + math.sin(pygame.time.get_ticks() * 0.01) * 2
        pygame.draw.circle(
            screen, YELLOW, (int(end_x), int(end_y)), int(pulse_size)
        )
        pygame.draw.circle(
            screen,
            (255, 100, 0),
            (int(end_x), int(end_y)),
            int(pulse_size * 0.6),
        )

    def level_up(self):
        """Улучшение косы"""
        self.level += 1
        self.damage += SCYTHE_MULTIPLIER_DAMAGE
        self.cooldown = max(700, self.cooldown - SCYTHE_MULTIPLIER_COOLDOWN)
        self.attack_range += SCYTHE_MULTIPLIER_RANGE

        if self.level % 2 == 0:
            if self.attack_angle + SCYTHE_MULTIPLIER_ANGLE > 360:
                self.attack_angle = 360
            else:
                self.attack_angle = min(
                    360, self.attack_angle + SCYTHE_MULTIPLIER_ANGLE
                )

        return True

    @property
    def is_weapon(self):
        return True
