from loguru import logger

from upgrades.upgrade import Upgrade
from weapons.magic_bullet_weapon import MagicBulletWeapon


class MagicBulletUpgrade(Upgrade):
    def __init__(self):
        super().__init__("Улучшение волшебной пули", "Увеличивает урон и а.спд")

    def apply(self, player):
        if weapon := player.weapons.get("magic_bullet"):
            weapon.level_up()
            logger.info(
                f"{weapon.name_ui} улучшена! {weapon.damage=}, {weapon.max_bullets=}"
            )
        player.add_weapon(MagicBulletWeapon())
