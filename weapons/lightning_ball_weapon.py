import math

from loguru import logger
import pygame

from settings import (
    LIGHT_BLUE,
    LIGHTNING_BALL_MULTIPLIER_BULLETS,
    LIGHTNING_BALL_MULTIPLIER_COOLDOWN,
    LIGHTNING_BALL_MULTIPLIER_DAMAGE,
)
from weapons.types.lightning_ball_projectile import LightningBallProjectile
from weapons.weapon import Weapon


class LightningBallWeapon(Weapon):
    def __init__(self):
        super().__init__(
            name="lightning_ball",
            name_ui="Шар молний",
            damage=2,
            cooldown=800,
            weapon_type="projectile",
        )
        self.projectiles = []
        self.lightning_effects = []
        self.max_projectiles = 2
        self.ball_speed = 5
        self.chain_range = 150
        self.max_chain_targets = 6
        self.chain_damage_reduction = 0.7

    def update(self, game):
        """Обновление шаров и обработка цепной молнии"""
        for ball in self.projectiles[:]:
            ball.update()

            if not ball.active:
                self.projectiles.remove(ball)
                continue

            # Проверяем столкновение шара
            if ball.is_collision():
                # Наносим урон первой цели
                # ball.target.take_damage(ball.damage, game)
                self.add_enemy_to_hit(enemy=ball.target)
                # Запускаем цепную молнию
                self.apply_chain_lightning(ball, game)

                # Деактивируем шар
                ball.active = False

    def apply_chain_lightning(self, source_ball, game):
        """Применяем цепную молнию от пораженной цели"""
        current_target = source_ball.target
        current_damage = source_ball.damage
        used_targets = {current_target}  # Уже пораженные цели
        chain_count = 0

        # Рисуем первую вспышку
        self.create_lightning_effect(source_ball, current_target)

        # Ищем следующие цели
        while chain_count < self.max_chain_targets:
            # Находим ближайшего врага в радиусе
            next_target = self.find_next_chain_target(
                current_target, used_targets, game.enemy_manager.enemies
            )

            if not next_target:
                break

            # Уменьшаем урон для следующей цели
            current_damage = int(current_damage * self.chain_damage_reduction)
            if current_damage < 1:
                break

            # Наносим урон
            # next_target.take_damage(current_damage, game)
            self.add_enemy_to_hit(enemy=next_target)

            # Рисуем молнию между целями
            self.create_lightning_effect(current_target, next_target)

            # Обновляем для следующего перехода
            used_targets.add(next_target)
            current_target = next_target
            chain_count += 1

    def find_next_chain_target(self, source, used_targets, all_enemies):
        """Находит следующую цель для цепной молнии"""
        potential_targets = []

        for enemy in all_enemies:
            if not enemy.active or enemy in used_targets:
                continue

            # Проверяем расстояние
            distance = math.sqrt(
                (source.rect.centerx - enemy.rect.centerx) ** 2
                + (source.rect.centery - enemy.rect.centery) ** 2
            )

            if distance <= self.chain_range:
                potential_targets.append((enemy, distance))

        if not potential_targets:
            return None

        # Берем ближайшего
        potential_targets.sort(key=lambda x: x[1])
        return potential_targets[0][0]

    def create_lightning_effect(self, source, target):
        """Создает визуальный эффект молнии между двумя точками"""
        # Это можно реализовать разными способами:
        # 1. Линия с зигзагами
        # 2. Анимация частиц
        # 3. Простая линия со свечением

        # Для простоты - добавим в список эффектов для отрисовки
        effect = {
            "start_pos": (source.rect.centerx, source.rect.centery),
            "end_pos": (target.rect.centerx, target.rect.centery),
            "lifetime": 3,  # кадров
            "width": 3,
        }

        self.lightning_effects.append(effect)

    def shoot(self, active_enemies):
        """Выстрел шарами молний"""
        if not active_enemies:
            return

        # Сколько шаров можем выпустить
        balls_to_shoot = self.max_projectiles - len(self.projectiles)

        if balls_to_shoot <= 0:
            return

        # Берем ближайших врагов
        enemies_by_distance = sorted(
            active_enemies, key=lambda e: self.owner.distance_to(e)
        )[:balls_to_shoot]

        # Создаем шары
        for enemy in enemies_by_distance:
            total_damage = self.damage + self.owner.get_damage()

            # Используем кастомный класс шара молнии
            ball = LightningBallProjectile(
                self.owner.rect.centerx,
                self.owner.rect.centery,
                enemy,
                total_damage,
            )
            ball.speed = self.ball_speed
            self.projectiles.append(ball)

    def draw(self, screen):
        """Отрисовка шаров и эффектов молний"""
        for ball in self.projectiles:
            ball.draw(screen)

        # Отрисовываем эффекты молний
        if hasattr(self, "lightning_effects"):
            for effect in self.lightning_effects[:]:
                # Рисуем молнию
                pygame.draw.line(
                    screen,
                    LIGHT_BLUE,
                    effect["start_pos"],
                    effect["end_pos"],
                    effect["width"],
                )

                # Добавляем свечение (более тонкую белую линию)
                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    effect["start_pos"],
                    effect["end_pos"],
                    max(1, effect["width"] - 2),
                )

                # Уменьшаем время жизни
                effect["lifetime"] -= 1
                if effect["lifetime"] <= 0:
                    self.lightning_effects.remove(effect)

    def level_up(self):
        self.level += 1

        self.max_projectiles += LIGHTNING_BALL_MULTIPLIER_BULLETS

        self.damage += LIGHTNING_BALL_MULTIPLIER_DAMAGE

        self.cooldown = max(
            500, self.cooldown - LIGHTNING_BALL_MULTIPLIER_COOLDOWN
        )

        if self.level % 2 == 0:
            self.max_chain_targets += 1
            logger.info(
                f"Цепная молния теперь поражает {self.max_chain_targets} целей!"
            )

        if self.level % 5 == 0:
            self.chain_range += 30
            logger.info(f"Дальность молнии увеличена до {self.chain_range}!")

        return True

    @property
    def is_weapon(self):
        return True
