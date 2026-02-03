from loguru import logger

from upgrades.upgrade import Upgrade


class HPRegenUpgrade(Upgrade):
    """Улучшение получаемого опыта"""

    def __init__(self):
        super().__init__(
            "Регенерация ХП",
            "Постепенно восстанавливает здоровье",
        )

    def apply(self, player):
        player.increase_hp_regeneration(1)
        logger.info("Регенерация ХП увеличена!")
