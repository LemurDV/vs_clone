from loguru import logger

from upgrades.upgrade import Upgrade
from weapons.lightning_ball_weapon import LightningBallWeapon


class LightningBallUpgrade(Upgrade):
    def __init__(self):
        super().__init__("Улучшение шаровой молнии", "Увеличивает урон")

    def apply(self, player):
        if weapon := player.weapons.get("lightning_ball"):
            weapon.level_up()
            logger.info(f"{weapon.name_ui} улучшена! Урон: {weapon.damage}")
            return
        player.add_weapon(LightningBallWeapon())
