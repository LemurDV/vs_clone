from settings import EXP_BOOST_MULTIPLIER
from upgrades.upgrade import Upgrade


class ExpBoostUpgrade(Upgrade):
    """Улучшение получаемого опыта"""

    def __init__(self):
        super().__init__("Улучшение получаемого опыта", "Улучшение получаемого опыта")

    def apply(self, player):
        player.increase_exp_boost(EXP_BOOST_MULTIPLIER)
        print(f"Урон увеличен! Множитель урона: {player.damage_multiplier}")
