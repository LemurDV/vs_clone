from settings import GREEN, RED

from .enemy import Enemy


class SlimeEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            width=25,
            height=25,
            color=GREEN,
            health=12,
            damage=5,
            experience_value=2,
            sprite_path="assets/enemies/slime.png",
        )
        self.speed = 0.5


class BossSlimeEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            width=40,
            height=40,
            color=GREEN,
            health=500,
            damage=30,
            experience_value=2000000,
            sprite_path="assets/enemies/boss_slime.png",
        )
        self.speed = 0.5


class BatEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            width=20,
            height=20,
            color=RED,
            health=11,
            damage=3,
            experience_value=5,
            sprite_path="assets/enemies/bat.png",
        )
        self.speed = 0.8
