from loot.loot_item import LootItem
from settings import *


class HealthPotion(LootItem):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.heal_amount = 20
        self.color = GREEN

    def apply(self, player):
        player.health = min(player.max_health, player.health + self.heal_amount)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 10)
