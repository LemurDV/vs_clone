from loguru import logger

from upgrades.upgrade import Upgrade
from weapons.scythe import ScytheWeapon


class ScytheUpgrade(Upgrade):
    def __init__(self):
        super().__init__("Улучшение косы", "Увеличивает урон")

    def apply(self, player):
        if weapon := player.weapons.get("scythe"):
            weapon.level_up()
            logger.info(f"{weapon.name_ui} улучшена! Урон: {weapon.damage}")
            return
        player.add_weapon(ScytheWeapon())
