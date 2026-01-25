from upgrades.upgrade import Upgrade


class HealthUpgrade(Upgrade):
    """Улучшение здоровья"""

    def __init__(self):
        super().__init__(
            "Усиление здоровья", "Увеличивает максимальное здоровье на 20"
        )

    def apply(self, player):
        """Применение улучшения"""
        player.max_health += 20
        player.health = player.max_health  # Восполняем здоровье
        print(f"Здоровье увеличено! Максимальное здоровье: {player.max_health}")
