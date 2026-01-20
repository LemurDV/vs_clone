import random

import pygame

from config import (
    BLUE,
    EXP_MULTIPLIER_PER_LEVEL,
    GREEN,
    HEIGHT,
    INITIAL_EXP_TO_NEXT_LEVEL,
    LEVEL_UP_DAMAGE_INCREASE,
    LEVEL_UP_HEALTH_INCREASE,
    LEVEL_UP_SHOOT_DELAY_DECREASE,
    MIN_SHOOT_DELAY,
    PLAYER_DAMAGE,
    PLAYER_HEALTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_DELAY,
    PLAYER_SPEED,
    RED,
    UPGRADE_ATTACK_SPEED_MULTIPLIER,
    UPGRADE_CRIT_CHANCE,
    UPGRADE_CRIT_MULTIPLIER,
    UPGRADE_DAMAGE_MULTIPLIER,
    UPGRADE_MAX_HEALTH_MULTIPLIER,
    UPGRADE_MOVEMENT_SPEED_MULTIPLIER,
    UPGRADE_VAMPIRISM_PERCENT,
    UPGRADES,
    UPGRADES_PER_LEVEL,
    WHITE,
    WIDTH,
)
from projectile import Projectile


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PLAYER_RADIUS
        self.speed = PLAYER_SPEED
        self.color = GREEN
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.exp = 0
        self.level = 1
        self.exp_to_next_level = INITIAL_EXP_TO_NEXT_LEVEL
        self.projectiles = []
        self.last_shot = 0
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.damage = PLAYER_DAMAGE
        self.is_alive = True

        # Статистика улучшений
        self.upgrades = {
            "damage": 0,
            "attack_speed": 0,
            "vampirism": 0,
            "crit_chance": 0,
            "max_health": 0,
            "movement_speed": 0,
        }

        # Базовые значения для расчетов
        self.base_damage = PLAYER_DAMAGE
        self.base_max_health = PLAYER_HEALTH
        self.base_shoot_delay = PLAYER_SHOOT_DELAY
        self.base_speed = PLAYER_SPEED

        # Вампиризм
        self.lifesteal = 0
        self.last_lifesteal_amount = 0

        # Критический удар
        self.crit_chance = 0
        self.last_crit = False

    def move(self, keys):
        """Движение игрока"""
        current_speed = self.speed

        # Применяем улучшение скорости
        if self.upgrades["movement_speed"] > 0:
            current_speed = self.base_speed * (
                UPGRADE_MOVEMENT_SPEED_MULTIPLIER
                ** self.upgrades["movement_speed"]
            )

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= current_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += current_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= current_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += current_speed

        # Ограничение движения в пределах экрана
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def shoot(self, current_time):
        """Стрельба во все 4 направления"""
        current_shoot_delay = self.shoot_delay

        # Применяем улучшение скорости атаки
        if self.upgrades["attack_speed"] > 0:
            current_shoot_delay = self.base_shoot_delay * (
                UPGRADE_ATTACK_SPEED_MULTIPLIER ** self.upgrades["attack_speed"]
            )
            current_shoot_delay = max(MIN_SHOOT_DELAY, current_shoot_delay)

        if current_time - self.last_shot > current_shoot_delay:
            # Стрельба в 4 направления
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in directions:
                damage, is_crit = self.get_damage()
                self.projectiles.append(
                    Projectile(self.x, self.y, dx, dy, damage, BLUE, is_crit)
                )
            self.last_shot = current_time

    def get_damage(self):
        """Получение урона с учетом улучшений и критов"""
        # Базовый урон с улучшениями
        base_damage = self.base_damage * (
            UPGRADE_DAMAGE_MULTIPLIER ** self.upgrades["damage"]
        )

        # Проверка на критический удар
        is_crit = False
        if self.upgrades["crit_chance"] > 0 and random.random() < (
            UPGRADE_CRIT_CHANCE * self.upgrades["crit_chance"]
        ):
            base_damage *= UPGRADE_CRIT_MULTIPLIER
            is_crit = True

        self.last_crit = is_crit  # Сохраняем для отображения
        return int(base_damage), is_crit

    def apply_vampirism(self, damage_dealt):
        """Применение вампиризма"""
        if self.upgrades["vampirism"] > 0:
            heal_amount = (
                damage_dealt
                * UPGRADE_VAMPIRISM_PERCENT
                * self.upgrades["vampirism"]
            )
            self.heal(heal_amount)
            self.last_lifesteal_amount = heal_amount

    def take_damage(self, amount):
        """Получение урона"""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return self.is_alive

    def heal(self, amount):
        """Лечение"""
        self.health = min(self.max_health, self.health + amount)
        return amount

    def add_exp(self, amount):
        """Добавление опыта"""
        self.exp += amount
        return self.check_level_up()

    def check_level_up(self):
        """Проверка повышения уровня"""
        if self.exp >= self.exp_to_next_level:
            # Отнимаем опыт для следующего уровня, но не повышаем уровень сразу
            # Уровень повысится после выбора улучшения в game.py
            return True
        return False

    def apply_level_up(self):
        """Применение повышения уровня (без улучшений)"""
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(
            self.exp_to_next_level * EXP_MULTIPLIER_PER_LEVEL
        )

        # Базовое улучшение характеристик (как было раньше)
        self.base_max_health += LEVEL_UP_HEALTH_INCREASE
        self.update_max_health()
        self.base_damage += LEVEL_UP_DAMAGE_INCREASE

        # Базовое улучшение скорости атаки
        if self.base_shoot_delay > MIN_SHOOT_DELAY:
            self.base_shoot_delay -= LEVEL_UP_SHOOT_DELAY_DECREASE

    def update_max_health(self):
        """Обновление максимального здоровья с учетом улучшений"""
        if self.upgrades["max_health"] > 0:
            self.max_health = int(
                self.base_max_health
                * (UPGRADE_MAX_HEALTH_MULTIPLIER ** self.upgrades["max_health"])
            )
        else:
            self.max_health = self.base_max_health

        # Здоровье не может превышать максимум
        if self.health > self.max_health:
            self.health = self.max_health

    def apply_upgrade(self, upgrade_type):
        """Применение выбранного улучшения"""
        if upgrade_type in self.upgrades:
            self.upgrades[upgrade_type] += 1

            # Специальная обработка для некоторых улучшений
            if upgrade_type == "max_health":
                self.update_max_health()
                # Восстанавливаем здоровье при улучшении максимального здоровья
                self.health = self.max_health
            elif upgrade_type == "vampirism":
                self.lifesteal = (
                    UPGRADE_VAMPIRISM_PERCENT * self.upgrades["vampirism"]
                )
            elif upgrade_type == "crit_chance":
                self.crit_chance = (
                    UPGRADE_CRIT_CHANCE * self.upgrades["crit_chance"]
                )

            return True
        return False

    def get_available_upgrades(self, count=UPGRADES_PER_LEVEL):
        """Получение списка доступных улучшений"""
        all_upgrades = list(UPGRADES.keys())

        # Можно добавить логику, чтобы некоторые улучшения выпадали чаще/реже
        # или исключать уже максимально прокачанные улучшения
        return random.sample(all_upgrades, min(count, len(all_upgrades)))

    def draw(self, screen):
        """Отрисовка игрока и его здоровья"""
        # Рисуем игрока
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), self.radius
        )
        pygame.draw.circle(
            screen, WHITE, (int(self.x), int(self.y)), self.radius, 2
        )

        # Рисуем полоску здоровья
        self.draw_health_bar(screen)

        # Рисуем иконку крита, если был критический удар
        if self.last_crit:
            self.draw_crit_indicator(screen)

    def draw_health_bar(self, screen):
        """Отрисовка полоски здоровья над игроком"""
        health_width = 50
        health_height = 6
        health_x = self.x - health_width // 2
        health_y = self.y - self.radius - 10
        health_ratio = self.health / self.max_health

        # Фон полоски здоровья
        pygame.draw.rect(
            screen, RED, (health_x, health_y, health_width, health_height)
        )
        # Заполнение здоровья
        pygame.draw.rect(
            screen,
            GREEN,
            (health_x, health_y, health_width * health_ratio, health_height),
        )

    def draw_crit_indicator(self, screen):
        """Отрисовка индикатора критического удара"""
        font = pygame.font.Font(None, 24)
        crit_text = font.render("CRIT!", True, (255, 255, 0))
        screen.blit(crit_text, (self.x + self.radius + 5, self.y - 10))

    def update_projectiles(self):
        """Обновление снарядов игрока"""
        for projectile in self.projectiles[:]:
            projectile.move()
            if projectile.is_off_screen():
                self.projectiles.remove(projectile)

    def get_stats(self):
        """Получение статистики игрока"""
        # Рассчитываем актуальные значения с учетом улучшений
        actual_damage, is_crit = self.get_damage()

        actual_shoot_delay = self.base_shoot_delay
        if self.upgrades["attack_speed"] > 0:
            actual_shoot_delay = self.base_shoot_delay * (
                UPGRADE_ATTACK_SPEED_MULTIPLIER ** self.upgrades["attack_speed"]
            )
            actual_shoot_delay = max(MIN_SHOOT_DELAY, actual_shoot_delay)

        actual_speed = self.base_speed
        if self.upgrades["movement_speed"] > 0:
            actual_speed = self.base_speed * (
                UPGRADE_MOVEMENT_SPEED_MULTIPLIER
                ** self.upgrades["movement_speed"]
            )

        return {
            "level": self.level,
            "exp": self.exp,
            "exp_to_next_level": self.exp_to_next_level,
            "health": self.health,
            "max_health": self.max_health,
            "damage": actual_damage,
            "shoot_delay": actual_shoot_delay,
            "movement_speed": actual_speed,
            "lifesteal": self.lifesteal * 100,  # в процентах
            "crit_chance": self.crit_chance * 100,  # в процентах
            "upgrades": self.upgrades.copy(),
        }

    def get_upgrade_description(self, upgrade_type):
        """Получение описания улучшения"""
        if upgrade_type in UPGRADES:
            upgrade = UPGRADES[upgrade_type]
            current_level = self.upgrades[upgrade_type]

            desc = f"{upgrade['icon']} {upgrade['name']} (Ур. {current_level + 1})\n"
            desc += f"{upgrade['description']}"

            # Добавляем информацию о текущем уровне
            if current_level > 0:
                desc += f"\nТекущий бонус: "
                if upgrade_type == "damage":
                    bonus = (UPGRADE_DAMAGE_MULTIPLIER**current_level - 1) * 100
                    desc += f"+{bonus:.0f}% урона"
                elif upgrade_type == "attack_speed":
                    bonus = (
                        1 - UPGRADE_ATTACK_SPEED_MULTIPLIER**current_level
                    ) * 100
                    desc += f"+{bonus:.0f}% скорости"
                elif upgrade_type == "vampirism":
                    bonus = UPGRADE_VAMPIRISM_PERCENT * current_level * 100
                    desc += f"{bonus:.0f}% вампиризма"
                elif upgrade_type == "crit_chance":
                    bonus = UPGRADE_CRIT_CHANCE * current_level * 100
                    desc += f"{bonus:.0f}% шанс крита"
                elif upgrade_type == "max_health":
                    bonus = (
                        UPGRADE_MAX_HEALTH_MULTIPLIER**current_level - 1
                    ) * 100
                    desc += f"+{bonus:.0f}% здоровья"
                elif upgrade_type == "movement_speed":
                    bonus = (
                        UPGRADE_MOVEMENT_SPEED_MULTIPLIER**current_level - 1
                    ) * 100
                    desc += f"+{bonus:.0f}% скорости"

            return desc
        return ""
