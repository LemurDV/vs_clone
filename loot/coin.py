import pygame

from loot.loot_item import LootItem
from settings import YELLOW


class Coin(LootItem):
    def __init__(self, x, y, value=1):
        super().__init__(x, y, width=10, height=10)
        self.value = value
        self.color = YELLOW
        self.sprite = pygame.image.load(
            "assets/items/gold_coin.jpg"
        ).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (25, 25))

    def apply(self, player):
        if hasattr(player, "coins"):
            player.coins += self.value

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
        # pygame.draw.circle(screen, self.color, self.rect.center, 8)
        # pygame.draw.circle(screen, (100, 100, 0), self.rect.center, 6)
