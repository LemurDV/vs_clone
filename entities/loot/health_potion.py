import pygame

from entities.loot.loot_item import LootItem
from settings import GREEN


class HealthPotion(LootItem):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.heal_amount = 10
        self.color = GREEN
        self.sprite = pygame.image.load(
            "assets/items/heal_potion.jpg"
        ).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (15, 15))

    def apply(self, player, game):
        player.heal(self.heal_amount)
        game.particle_system.add_heal_text(
            x=player.x,
            y=player.y,
            heal=self.heal_amount,
        )

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
