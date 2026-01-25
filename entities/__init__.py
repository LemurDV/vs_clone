from settings import *

from .enemy import Enemy


class SlimeEnemy(Enemy):
    """Слайм - медленный враг с умеренным здоровьем"""

    def __init__(self, x, y):
        super().__init__(x, y, 25, 25, GREEN, 30, 5, 10)
        self.speed = 1.5


class BatEnemy(Enemy):
    """Летучая мышь - быстрый враг с малым здоровьем"""

    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, RED, 15, 3, 5)
        self.speed = 3.0
