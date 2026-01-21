import math
import random

import pygame

from config import (
    ENEMY_MAX_EXP,
    ENEMY_MAX_HEALTH,
    ENEMY_MAX_RADIUS,
    ENEMY_MAX_SPEED,
    ENEMY_MIN_EXP,
    ENEMY_MIN_HEALTH,
    ENEMY_MIN_RADIUS,
    ENEMY_MIN_SPEED,
    HEIGHT,
    RED,
    WHITE,
    WIDTH,
    YELLOW,
)


class Enemy:
    def __init__(self):
        # Появление с краев экрана
        side = random.randint(0, 3)
        if side == 0:  # сверху
            self.x = random.randint(0, WIDTH)
            self.y = -20
        elif side == 1:  # справа
            self.x = WIDTH + 20
            self.y = random.randint(0, HEIGHT)
        elif side == 2:  # снизу
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT + 20
        else:  # слева
            self.x = -20
            self.y = random.randint(0, HEIGHT)

        self.radius = random.randint(ENEMY_MIN_RADIUS, ENEMY_MAX_RADIUS)
        self.speed = random.uniform(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        self.color = RED
        self.health = random.randint(ENEMY_MIN_HEALTH, ENEMY_MAX_HEALTH)
        self.max_health = self.health
        self.exp_value = random.randint(ENEMY_MIN_EXP, ENEMY_MAX_EXP)
        self.is_alive = True

    def move(self, target_x, target_y):
        """Движение к цели"""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed

    def take_damage(self, amount,  color):
        """Получение урона с учетом критов"""
        # self.color = color

        self.health -= amount
        # was_alive = self.is_alive
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

        return self.is_alive, amount

    def draw(self, screen):
        """Отрисовка врага и его здоровья"""
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), self.radius
        )
        pygame.draw.circle(
            screen, WHITE, (int(self.x), int(self.y)), self.radius, 2
        )

        # Рисуем полоску здоровья, если враг поврежден
        if self.health < self.max_health:
            self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        """Отрисовка полоски здоровья над врагом"""
        health_width = self.radius * 2
        health_height = 4
        health_x = self.x - self.radius
        health_y = self.y - self.radius - 8
        health_ratio = self.health / self.max_health

        # Фон полоски здоровья
        pygame.draw.rect(
            screen, RED, (health_x, health_y, health_width, health_height)
        )
        # Заполнение здоровья
        pygame.draw.rect(
            screen,
            YELLOW,
            (health_x, health_y, health_width * health_ratio, health_height),
        )

    def is_off_screen(self):
        """Проверка, вышел ли враг за пределы экрана"""
        margin = 50
        return (
            self.x < -margin
            or self.x > WIDTH + margin
            or self.y < -margin
            or self.y > HEIGHT + margin
        )

    def check_collision_with_player(self, player_x, player_y, player_radius):
        """Проверка столкновения с игроком"""
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < player_radius + self.radius
