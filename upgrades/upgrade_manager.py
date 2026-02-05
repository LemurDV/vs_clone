import random

from upgrades import (
    AuraUpgrade,
    DamageUpgrade,
    ExpBoostUpgrade,
    HealthUpgrade,
    HPRegenUpgrade,
    LightningBallUpgrade,
    MagicBulletUpgrade,
    MagnetRadiusUpgrade,
    ScytheUpgrade,
)


class UpgradeManager:
    def __init__(self):
        self.all_upgrades = []
        self.initialize_upgrades()

    def initialize_upgrades(self):
        self.all_upgrades.extend(
            [
                MagicBulletUpgrade(),
                AuraUpgrade(),
                LightningBallUpgrade(),
                ScytheUpgrade(),
                DamageUpgrade(),
                HealthUpgrade(),
                MagnetRadiusUpgrade(),
                ExpBoostUpgrade(),
                HPRegenUpgrade(),
            ]
        )

    def get_random_upgrades(self, count=3, player=None):
        available = self.all_upgrades.copy()
        selected = []

        while len(selected) < count and available:
            upgrade = random.choice(available)
            available.remove(upgrade)
            selected.append(upgrade)

        return selected

    def add_new_upgrade(self, upgrade):
        self.all_upgrades.append(upgrade)
