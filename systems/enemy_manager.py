import random

from entities import SlimeEnemy, BatEnemy
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class EnemyManager:
    def __init__(self):
        self.enemies = []

    def spawn_enemy(self, current_level: int):
        """Создание нового врага"""
        # Ограничение по количеству врагов в зависимости от уровня
        max_enemies = 100
        if len(self.enemies) >= max_enemies:
            return

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

        if random.random() < 0.5:
            enemy = SlimeEnemy(x, y)
        else:
            enemy = BatEnemy(x, y)

        self.enemies.append(enemy)
