from settings import *

from .enemy import Enemy


class SlimeEnemy(Enemy):
    """Слайм - медленный враг с умеренным здоровьем"""

    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            width=25,
            height=25,
            color=GREEN,
            health=30,
            damage=5,
            experience_value=30,
            sprite_path="assets/enemies/slime.png",
        )
        self.speed = 0.8


class BossSlimeEnemy(Enemy):
    """Босс слайм"""

    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            width=40,
            height=40,
            color=GREEN,
            health=100,
            damage=30,
            experience_value=200000,
            sprite_path="assets/enemies/boss_slime.png",
        )
        self.speed = 0.8


class BatEnemy(Enemy):
    """Летучая мышь - быстрый враг с малым здоровьем"""

    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            width=20,
            height=20,
            color=RED,
            health=15,
            damage=3,
            experience_value=20,
            sprite_path="assets/enemies/bat.png",
        )
        self.speed = 1.5
