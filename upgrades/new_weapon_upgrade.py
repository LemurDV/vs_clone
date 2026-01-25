from upgrades.upgrade import Upgrade
from weapons.aura_weapon import AuraWeapon
from weapons.magic_bullet_weapon import MagicBulletWeapon


class NewWeaponUpgrade(Upgrade):
    """Улучшение - новое оружие"""

    def __init__(self, weapon_class):
        self.weapon_class = weapon_class
        weapon_instance = weapon_class()
        super().__init__(
            f"Новое оружие: {weapon_instance.name}", weapon_instance.name
        )
        self.weapon_instance = weapon_instance

    def apply(self, player):
        """Применение улучшения"""
        # Проверяем, есть ли уже такое оружие
        for weapon in player.weapons:
            if isinstance(weapon, self.weapon_class):
                # Если есть - улучшаем его
                weapon.level_up()
                print(
                    f"Оружие '{weapon.name}' улучшено до уровня {weapon.level}"
                )
                return

        # Если нет - добавляем новое
        new_weapon = self.weapon_class()
        player.add_weapon(new_weapon)
        print(f"Добавлено новое оружие: {new_weapon.name}")

    def is_compatible(self, player):
        """Совместимо ли улучшение с игроком"""
        # Для оружия - проверяем, не достигло ли оно максимального уровня
        for weapon in player.weapons:
            if isinstance(weapon, self.weapon_class):
                return weapon.level < weapon.max_level
        return True

    @property
    def is_weapon(self):
        return True
