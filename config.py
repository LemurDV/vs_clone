import pygame


pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1000, 700
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
PURPLE = (180, 70, 255)
ORANGE = (255, 150, 50)
CYAN = (0, 200, 255)

# Шрифты
FONT_SMALL = pygame.font.SysFont(None, 28)
FONT_MEDIUM = pygame.font.SysFont(None, 36)
FONT_LARGE = pygame.font.SysFont(None, 48)

# Настройки игрока
PLAYER_RADIUS = 15
PLAYER_MOVEMENT_SPEED = 3
PLAYER_HEALTH = 100
PLAYER_DAMAGE = 10
PLAYER_SHOOT_DELAY = 800  # мс

# Настройки врагов
ENEMY_MIN_RADIUS = 10
ENEMY_MAX_RADIUS = 30
ENEMY_MIN_SPEED = 1.5
ENEMY_MAX_SPEED = 3.0
ENEMY_MIN_HEALTH = 20
ENEMY_MAX_HEALTH = 40
ENEMY_MIN_EXP = 20
ENEMY_MAX_EXP = 40
MAX_ENEMIES_ON_SCREEN = 100

# Настройки снарядов
PROJECTILE_RADIUS = 5
PROJECTILE_SPEED = 5

# Настройки опыта
EXP_ORB_RADIUS = 6
EXP_ORB_SPEED = 2
EXP_MAGNET_DISTANCE = 100
EXP_ORB_SPEED_UP_DISTANCE = 50

# Настройки волн
INITIAL_ENEMIES_PER_WAVE = 30
ENEMY_SPAWN_DELAY = 500
MIN_ENEMY_SPAWN_DELAY = 200
ENEMY_SPAWN_DELAY_DECREASE = 1  # на волну
ENEMY_INCREASE_PER_WAVE = 25
WAVE_REWARD_EXP = 50

# Уровень сложности
LEVEL_UP_HEALTH_INCREASE = 10
LEVEL_UP_DAMAGE_INCREASE = 2
LEVEL_UP_SHOOT_DELAY_DECREASE = 10  # мс
MIN_SHOOT_DELAY = 200
INITIAL_EXP_TO_NEXT_LEVEL = 30
EXP_MULTIPLIER_PER_LEVEL = 1.5

# Система улучшений
UPGRADES = {
    "damage": {
        "name": "Усиление атаки",
        "description": "Увеличивает урон на 30%",
        "color": (255, 100, 100),
        "icon": "⚔️",
    },
    "attack_speed": {  # TODO: тоже поправить, сильно быстро бахает(
        "name": "Скорострельность",
        "description": "Увеличивает скорость атаки на 25%",
        "color": (100, 200, 255),
        "icon": "⚡",
    },
    "vampirism": {
        "name": "Вампиризм",
        "description": "Восстанавливает 10% от нанесенного урона",
        "color": (200, 50, 150),
        "icon": "🩸",
    },
    "crit_chance": {
        "name": "Критический удар",
        "description": "Шанс нанести 200% урона",
        "color": (255, 200, 50),
        "icon": "💥",
    },
    "max_health": {
        "name": "Живучесть",
        "description": "Увеличивает максимальное здоровье на 20%",
        "color": (100, 255, 100),
        "icon": "❤️",
    },
    # TODO: исрпавить ее. поломалась при выборе апгрейда)
    # "movement_speed": {
    #     "name": "Скорость",
    #     "description": "Увеличивает скорость движения на 20%",
    #     "color": (200, 100, 255),
    #     "icon": "👟",
    # },
    "aura": {
        "name": "Магическая аура",
        "description": "Наносит урон врагам рядом с вами. Улучшение: +20% урона, +10 радиуса",
        "color": (180, 70, 255),
        "icon": "🌀",
        "type": "weapon",
        "damage": 2,
        "radius": 80,
        "cooldown": 800,
    },
    "orbiting": {
        "name": "Орбитальные сферы",
        "description": "Сферы, вращающиеся вокруг вас. Улучшение: +20% урона, +1 сфера",
        "color": (50, 200, 50),
        "icon": "🪐",
        "type": "weapon",
        "damage": 5,
        "orbit_radius": 50,
        "speed": 0.05,
        "cooldown": 500,
    },
    "melee": {
        "name": "Взрывная волна",
        "description": "Волна урона вокруг вас. Улучшение: +20% урона, -0.1с кулдаун",
        "color": (255, 150, 50),
        "icon": "💥",
        "type": "weapon",
        "damage": 15,
        "radius": 60,
        "cooldown": 3000,
    },
}

LEVEL_DIFFICULTY = {
    1: {
        "enemy_multiplier": 0.8,
        "enemy_speed_multiplier": 0.8,
        "player_health_multiplier": 1.2,
        "wave_reward_multiplier": 1.2,
    },
    2: {
        "enemy_multiplier": 1.0,
        "enemy_speed_multiplier": 1.0,
        "player_health_multiplier": 1.0,
        "wave_reward_multiplier": 1.0,
    },
    3: {
        "enemy_multiplier": 1.3,
        "enemy_speed_multiplier": 1.2,
        "player_health_multiplier": 0.8,
        "wave_reward_multiplier": 0.8,
    },
}

# Настройки карт
MAP_WIDTH = 1000  # Ширина карты по умолчанию
MAP_HEIGHT = 1000  # Высота карты по умолчанию

# Зона безопасности для движения камеры
CAMERA_SAFE_ZONE = 100

# Пути к картам
MAP_PATHS = {
    1: "assets/maps/level1_map.jpg",
    2: "assets/maps/level2_map.jpg",
    3: "assets/maps/level3_map.jpg",
}

# Параметры улучшений
UPGRADE_DAMAGE_MULTIPLIER = 1.1  # +10% урона
UPGRADE_ATTACK_SPEED_MULTIPLIER = 0.05  # -5% задержки (быстрее на 25%)
UPGRADE_VAMPIRISM_PERCENT = 0.05  # 10% вампиризма
UPGRADE_CRIT_CHANCE = 0.05  # 20% шанс крита
UPGRADE_CRIT_MULTIPLIER = 2.0  # 200% урона при крите
UPGRADE_MAX_HEALTH_MULTIPLIER = 0.05  # +5% здоровья
UPGRADE_MOVEMENT_SPEED_MULTIPLIER = 0.05  # +5% скорости

# Настройки отображения улучшений
UPGRADES_PER_LEVEL = 3  # Количество предлагаемых улучшений
UPGRADE_BUTTON_WIDTH = 250
UPGRADE_BUTTON_HEIGHT = 100
UPGRADE_BUTTON_MARGIN = 20
