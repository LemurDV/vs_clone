from upgrades.upgrade import Upgrade


class SpeedUpgrade(Upgrade):
    def __init__(self):
        super().__init__(
            "Увеличение скорости", "Увеличивает скорость передвижения на 20%"
        )

    def apply(self, player):
        player.speed *= 1.2
        print(f"Скорость увеличена! Текущая скорость: {player.speed}")
