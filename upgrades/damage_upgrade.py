from upgrades.upgrade import Upgrade


class DamageUpgrade(Upgrade):
    """Улучшение урона"""

    def __init__(self):
        super().__init__(
            name="Усиление урона",
            description="Увеличивает урон на 20%",
            image_path="assets/upgrades/damage.png",
        )

    def apply(self, player):
        """Применение улучшения"""
        player.increase_damage(4)
        print(f"Урон увеличен! Множитель урона: {player.damage_multiplier}")
