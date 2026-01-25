import pygame


# Инициализация Pygame
pygame.init()

# Размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Игровые константы
FPS = 60
PLAYER_SPEED = 3
ENEMY_SPEED = 2
SPAWN_RATE = 1000  # ms
EXPERIENCE_ORB_LIFETIME = 5000  # ms

# Уровни
LEVELS = {
    1: {"exp_required": 10, "max_enemies": 10},
    2: {"exp_required": 20, "max_enemies": 15},
    3: {"exp_required": 30, "max_enemies": 20},
    4: {"exp_required": 40, "max_enemies": 25},
    5: {"exp_required": 50, "max_enemies": 30},
}
