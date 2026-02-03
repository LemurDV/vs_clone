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
    """Управление пулом улучшений и их выдачей"""

    def __init__(self):
        self.all_upgrades = []
        self.initialize_upgrades()

    def initialize_upgrades(self):
        """Инициализация всех доступных улучшений"""
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
        """Получить случайные улучшения (с учетом уже имеющихся)"""
        available = self.all_upgrades.copy()

        # Фильтрация: не показывать одно и то же улучшение дважды за выбор
        selected = []

        while len(selected) < count and available:
            # Выбираем случайное улучшение
            upgrade = random.choice(available)
            available.remove(upgrade)

            # Проверяем, совместимо ли улучшение с игроком
            if hasattr(upgrade, "is_compatible") and player:
                if not upgrade.is_compatible(player):
                    continue

            selected.append(upgrade)

            # Если это оружие, удаляем его из пула, чтобы не появлялось снова
            if hasattr(upgrade, "is_weapon") and upgrade.is_weapon:
                # Удаляем все экземпляры этого оружия из пула
                available = [
                    u
                    for u in available
                    if not (
                        hasattr(u, "is_weapon")
                        and u.__class__ == upgrade.__class__
                    )
                ]

        return selected

    def add_new_upgrade(self, upgrade):
        """Добавить новое улучшение в пул"""
        self.all_upgrades.append(upgrade)
