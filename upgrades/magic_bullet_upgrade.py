from loguru import logger

from upgrades.upgrade import Upgrade
from weapons.magic_bullet_weapon import MagicBulletWeapon


class MagicBulletUpgrade(Upgrade):
    def __init__(self):
        super().__init__(
            name="Улучшение волшебной пули",
            description="Увеличивает урон и а.спд",
            image_path="assets/upgrades/magic_bullet.png",
        )

    def apply(self, player):
        if weapon := player.weapons.get("magic_bullet"):
            weapon.level_up()
            logger.info(
                f"{weapon.name_ui} улучшена! {weapon.damage=}, {weapon.max_projectiles=}"
            )
            return
        player.add_weapon(MagicBulletWeapon())
