from upgrades.upgrade import Upgrade


class SpeedUpgrade(Upgrade):
    def __init__(self):
        super().__init__(
            name="Увеличение скорости",
            description="Увеличивает скорость передвижения на 20%",
            image_path="assets/upgrades/speed.png",
        )

    def apply(self, player):
        player.speed *= 1.2
        print(f"Скорость увеличена! Текущая скорость: {player.speed}")
