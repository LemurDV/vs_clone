from upgrades.upgrade import Upgrade


class DamageUpgrade(Upgrade):
    """Улучшение урона"""

    def __init__(self):
        super().__init__("Усиление урона", "Увеличивает урон на 20%")

    def apply(self, player):
        """Применение улучшения"""
        player.damage_multiplier *= 1.2
        print(f"Урон увеличен! Множитель урона: {player.damage_multiplier}")
