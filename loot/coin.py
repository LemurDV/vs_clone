import pygame

from loot.loot_item import LootItem
from settings import YELLOW


class Coin(LootItem):
    def __init__(self, x, y, value=1):
        super().__init__(x, y)
        self.value = value
        self.color = YELLOW

    def apply(self, player):
        if hasattr(player, "coins"):
            player.coins += self.value

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 8)
        pygame.draw.circle(screen, (100, 100, 0), self.rect.center, 6)
