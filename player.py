import math

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

    def move(self, keys):
        """Движение игрока"""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        # Ограничение движения в пределах экрана
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def shoot(self, current_time):
        """Стрельба во все 4 направления"""
        if current_time - self.last_shot > self.shoot_delay:
            # Стрельба в 4 направления
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in directions:
                self.projectiles.append(
                    Projectile(self.x, self.y, dx, dy, self.damage, BLUE)
                )
            self.last_shot = current_time

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

    def add_exp(self, amount):
        """Добавление опыта"""
        self.exp += amount
        return self.check_level_up()

    def check_level_up(self):
        """Проверка повышения уровня"""
        if self.exp >= self.exp_to_next_level:
            self.level_up()
            return True
        return False

    def level_up(self):
        """Повышение уровня"""
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(
            self.exp_to_next_level * EXP_MULTIPLIER_PER_LEVEL
        )
        self.max_health += LEVEL_UP_HEALTH_INCREASE
        self.health = self.max_health
        self.damage += LEVEL_UP_DAMAGE_INCREASE

        # Уменьшение задержки стрельбы
        if self.shoot_delay > MIN_SHOOT_DELAY:
            self.shoot_delay -= LEVEL_UP_SHOOT_DELAY_DECREASE

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

    def update_projectiles(self):
        """Обновление снарядов игрока"""
        for projectile in self.projectiles[:]:
            projectile.move()
            if projectile.is_off_screen():
                self.projectiles.remove(projectile)

    def get_stats(self):
        """Получение статистики игрока"""
        return {
            "level": self.level,
            "exp": self.exp,
            "exp_to_next_level": self.exp_to_next_level,
            "health": self.health,
            "max_health": self.max_health,
            "damage": self.damage,
            "shoot_delay": self.shoot_delay,
        }
