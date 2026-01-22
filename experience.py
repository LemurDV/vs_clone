import math

import pygame

from config import (
    EXP_MAGNET_DISTANCE,
    EXP_ORB_RADIUS,
    EXP_ORB_SPEED,
    WHITE,
    YELLOW,
)


class Experience:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.world_x = x  # Мировые координаты
        self.world_y = y  # Мировые координаты
        self.radius = EXP_ORB_RADIUS
        self.value = value
        self.color = YELLOW
        self.speed = EXP_ORB_SPEED
        self.collected = False

    def move_towards(self, target_world_x, target_world_y):
        """Движение к цели в мировых координатах"""
        dx = target_world_x - self.world_x
        dy = target_world_y - self.world_y

        distance = max(0.1, (dx ** 2 + dy ** 2) ** 0.5)

        # Ускоряемся при приближении к игроку
        speed_multiplier = 1.0
        if distance < 100:
            speed_multiplier = 2.0

        dx = (dx / distance) * self.speed * speed_multiplier
        dy = (dy / distance) * self.speed * speed_multiplier

        self.world_x += dx
        self.world_y += dy

    def move(self, player_x, player_y):
        self.move_towards(player_x, player_y)
        """Движение к игроку при приближении"""
        # dx = player_x - self.x
        # dy = player_y - self.y
        # dist = math.sqrt(dx * dx + dy * dy)
        #
        # # Магнитный эффект: притягивание к игроку на близкой дистанции
        # if dist < EXP_MAGNET_DISTANCE and dist > 0:
        #     self.x += dx / dist * self.speed
        #     self.y += dy / dist * self.speed

    def draw(self, screen):
        """Отрисовка орба опыта"""
        # Основной круг
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), self.radius
        )

        # Контур
        pygame.draw.circle(
            screen, WHITE, (int(self.x), int(self.y)), self.radius, 1
        )

        # Блик
        pygame.draw.circle(
            screen,
            (255, 255, 200),
            (int(self.x - self.radius // 3), int(self.y - self.radius // 3)),
            self.radius // 3,
        )

    def check_collection(self, player_x, player_y, player_radius):
        """Проверка сбора игроком"""
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < player_radius + self.radius:
            self.collected = True
            return True
        return False
