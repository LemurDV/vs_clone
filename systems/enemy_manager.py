import random

from loguru import logger
import pygame

from entities import BatEnemy, BossSlimeEnemy, SlimeEnemy
from settings import MAX_ENEMIES_ON_SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH


class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.start_time = pygame.time.get_ticks()
        self.current_difficulty = 1.0
        self.difficulty_check_time = 0
        self.elapsed_minutes = 0

        # Настройки прогрессии сложности
        self.difficulty_increase_interval = 60000  # Каждую минуту (60000 мс)
        self.difficulty_increase_amount = 0.2

        # Множители для разных параметров врагов
        self.health_multiplier = 1.0
        self.damage_multiplier = 1.0
        self.experience_multiplier = 1.0  # Начинаем с 1.0!
        self.speed_multiplier = 1.0

        # На сколько увеличивать каждый множитель за минуту
        self.health_increase_per_minute = 0.15  # +15% здоровья в минуту
        self.damage_increase_per_minute = 0.1  # +10% урона в минуту
        self.exp_increase_per_minute = 20.0
        self.speed_increase_per_minute = 0.05  # +5% скорости в минуту

    def update_difficulty(self):
        """Обновляем сложность с течением времени"""
        current_time = pygame.time.get_ticks()
        new_elapsed_minutes = (current_time - self.start_time) // 60000

        if new_elapsed_minutes > self.elapsed_minutes:
            self.spawn_boss()
            self.elapsed_minutes = new_elapsed_minutes

            self.current_difficulty += self.difficulty_increase_amount
            self.health_multiplier += self.health_increase_per_minute
            self.damage_multiplier += self.damage_increase_per_minute
            self.experience_multiplier += self.exp_increase_per_minute
            self.speed_multiplier += self.speed_increase_per_minute

            logger.info(f"Сложность увеличена! Минута #{self.elapsed_minutes}")
            logger.info(f"Множитель опыта: x{self.experience_multiplier:.1f}")
            logger.info(f"Множитель здоровья: x{self.health_multiplier:.1f}")
            logger.info(f"Текущая сложность: {self.current_difficulty:.1f}")

    def spawn_boss(self):
        x, y = self.randomize_x_y()
        boss = BossSlimeEnemy(x=x, y=y)
        self.enemies.append(boss)

    def randomize_x_y(self):
        side = random.randint(0, 3)
        if side == 0:  # Сверху
            x = random.randint(0, SCREEN_WIDTH)
            y = -20
        elif side == 1:  # Справа
            x = SCREEN_WIDTH + 20
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # Снизу
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 20
        else:  # Слева
            x = -20
            y = random.randint(0, SCREEN_HEIGHT)

        return x, y

    def spawn_enemy(self, current_level: int):
        """Создание нового врага с учетом сложности"""
        self.update_difficulty()

        max_enemies = MAX_ENEMIES_ON_SCREEN + (current_level * 5)
        if len(self.enemies) >= max_enemies:
            return

        x, y = self.randomize_x_y()

        # Выбор типа врага
        enemy_type = random.random()
        if enemy_type < 0.5:
            base_enemy = SlimeEnemy(x, y)
        else:
            base_enemy = BatEnemy(x, y)

        # Применяем множители сложности
        self.apply_difficulty_modifiers(base_enemy)
        self.enemies.append(base_enemy)

    def apply_difficulty_modifiers(self, enemy):
        """Применяем модификаторы сложности к врагу"""
        enemy.health = int(enemy.health * self.health_multiplier)
        enemy.max_health = int(enemy.max_health * self.health_multiplier)

        enemy.damage = int(enemy.damage * self.damage_multiplier)

        enemy.experience_value = int(
            enemy.experience_value * self.experience_multiplier
        )

        enemy.speed = enemy.speed * self.speed_multiplier

    def get_current_difficulty_stats(self):
        return {
            "difficulty": self.current_difficulty,
            "exp_multiplier": self.experience_multiplier,
            "health_multiplier": self.health_multiplier,
            "damage_multiplier": self.damage_multiplier,
            "speed_multiplier": self.speed_multiplier,
            "elapsed_minutes": self.elapsed_minutes,
        }
