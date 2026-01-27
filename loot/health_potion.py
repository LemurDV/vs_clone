import pygame

from loot.loot_item import LootItem
from settings import GREEN


class HealthPotion(LootItem):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.heal_amount = 20
        self.color = GREEN
        self.sprite = pygame.image.load(
            "assets/items/heal_potion.jpg"
        ).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (15, 15))

    def apply(self, player):
        player.health = min(player.max_health, player.health + self.heal_amount)

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
        # pygame.draw.circle(screen, self.color, self.rect.center, 10)
