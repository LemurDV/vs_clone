from upgrades.upgrade import Upgrade


class AuraUpgrade(Upgrade):
    def __init__(self):
        super().__init__(
            "Улучшение ауры", "Увеличивает радиус и урон ауры на 20%"
        )

    def apply(self, player):
        for weapon in player.weapons:
            if weapon.name == "Аура":
                weapon.radius *= 1.2
                weapon.damage *= 1.2
                print(
                    f"Аура улучшена! Радиус: {weapon.radius}, Урон: {weapon.damage}"
                )
                break
