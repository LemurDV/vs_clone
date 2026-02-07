from loguru import logger

from upgrades.upgrade import Upgrade


class HPRegenUpgrade(Upgrade):
    """Улучшение получаемого опыта"""

    def __init__(self):
        super().__init__(
            name="Регенерация ХП",
            description="Постепенно восстанавливает здоровье",
            image_path="assets/upgrades/hp_regen.png",
        )

    def apply(self, player):
        player.increase_hp_regeneration(1)
        logger.info("Регенерация ХП увеличена!")
