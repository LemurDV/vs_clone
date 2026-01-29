import random

from loot.coin import Coin
from loot.experience_orb import ExperienceOrb
from loot.health_potion import HealthPotion


class LootManager:
    """Управление дропом с врагов"""

    def __init__(self):
        self.drop_chances = {
            "health_potion": 0.1,
            "coin": 0.15,
        }

    def drop_from_enemy(self, enemy, game):
        """Создать лут с врага"""
        game.add_loot_item(
            ExperienceOrb(
                enemy.rect.centerx,
                enemy.rect.centery,
                enemy.experience_value,
            ),
        )

        # Дополнительный лут
        for loot_type, chance in self.drop_chances.items():
            if random.random() < chance:
                self.create_loot(
                    loot_type, enemy.rect.centerx, enemy.rect.centery, game
                )

    def create_loot(self, loot_type, x, y, game):
        """Создать конкретный лут"""
        if loot_type == "health_potion":
            item = HealthPotion(x, y)
        elif loot_type == "coin":
            item = Coin(x, y, random.randint(1, 3))
        else:
            return

        game.add_loot_item(item)
