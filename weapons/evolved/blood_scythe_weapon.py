from weapons import ScytheWeapon
from weapons.weapon import WeaponTypes


class BloodScytheWeapon(ScytheWeapon):
    def __init__(
        self,
        name: str = "blood_scythe",
        name_ui: str = "Кровавая коса",
        damage: int = 15,
        cooldown: int = 1_500,
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
        self.attack_angle = 379
        self.attack_duration = 600
        self.attack_start_time = 0
        self.is_attacking = False

        self.attack_direction = 0

        # Для анимации (если захотим визуализировать без спрайта)
        self.attack_progress = 0  # 0..1
