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
ENEMY_SPEED = 2
SPAWN_RATE = 100  # ms
EXPERIENCE_ORB_LIFETIME = 5000  # ms

# Настройки игрока
PLAYER_SPEED = 3
MAGNET_RADIUS = 100
MAGNET_RADIUS_MULTIPLIER = 50
EXP_BOOST_MULTIPLIER = 0.04  # 4%?)

# Настройки шариков опыта
EXP_ORB_RADIUS = 5
EXP_ORB_SPEED = 5

# Уровни
BASE_EXPERIENCE = 100
EXPERIENCE_MULTIPLIER = 1.7
# LEVELS = {
#     1: {"exp_required": 100, "max_enemies": 40},
#     2: {"exp_required": 20, "max_enemies": 80},
#     3: {"exp_required": 30, "max_enemies": 160},
#     4: {"exp_required": 40, "max_enemies": 200},
#     5: {"exp_required": 50, "max_enemies": 400},
# }

# Настройки уровней оружий
AURA_MULTIPLIER_DAMAGE = 2
AURA_MULTIPLIER_RADIUS = 8
