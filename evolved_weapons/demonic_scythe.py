from weapons import ScytheWeapon
from weapons.weapon import WeaponTypes


class DemonicScytheWeapon(ScytheWeapon):
    def __init__(
        self,
        name: str = "demonic_scythe",
        name_ui: str = "Демоническая коса",
        damage: int = 15,
        cooldown: int = 800,
        weapon_type=WeaponTypes.MELEE,
    ):
        super().__init__(
            name=name,
            name_ui=name_ui,
            damage=damage,
            cooldown=cooldown,
            weapon_type=weapon_type,
            causes_bleeding_chance=1.0,
        )

        self.attack_range = 150
        self.attack_angle = 190
        self.attack_duration = 900
        self.attack_start_time = 0
        self.is_attacking = False

        self.attack_direction = 0

        # Для анимации (если захотим визуализировать без спрайта)
        self.attack_progress = 0  # 0..1

    def level_up(self):
        return False
