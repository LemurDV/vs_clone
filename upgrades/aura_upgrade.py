from loguru import logger

from upgrades.upgrade import Upgrade
from weapons.aura_weapon import AuraWeapon


class AuraUpgrade(Upgrade):
    def __init__(self):
        super().__init__(
            name="Улучшение ауры",
            description="Увеличивает радиус и урон ауры на 20%",
            image_path="assets/upgrades/aura.png",
        )

    def apply(self, player):
        if weapon := player.weapons.get("aura"):
            weapon.level_up()
            logger.info(f"{weapon.name_ui} улучшена! Урон: {weapon.damage}")
            return
        player.add_weapon(AuraWeapon())
