from loguru import logger

from settings import MAGNET_RADIUS_MULTIPLIER
from upgrades.upgrade import Upgrade


class MagnetRadiusUpgrade(Upgrade):
    def __init__(self):
        super().__init__(
            "Улучшение радиуса сбора", "Увеличивает радиус сбора предметов"
        )

    def apply(self, player):
        """Применение улучшения"""
        player.increase_magnet_radius(MAGNET_RADIUS_MULTIPLIER)
        logger.info(
            f"Урон увеличен! Множитель урона: {player.damage_multiplier}"
        )
