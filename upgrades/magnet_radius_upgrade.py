from loguru import logger

from settings import MAGNET_RADIUS_MULTIPLIER
from upgrades.upgrade import Upgrade


class MagnetRadiusUpgrade(Upgrade):
    def __init__(self):
        super().__init__(
            name="Улучшение радиуса сбора",
            description="Увеличивает радиус сбора предметов",
            image_path="assets/upgrades/magnet_radius.png",
        )

    def apply(self, player):
        """Применение улучшения"""
        player.increase_magnet_radius(MAGNET_RADIUS_MULTIPLIER)
        logger.info("Радиус сбора увеличен!")
