from loot.loot_item import LootItem
from settings import pygame


class ExperienceOrb(LootItem):
    """Сфера опыта"""

    def __init__(self, x, y, value):
        super().__init__(
            x=x,
            y=y,
            width=20,
            height=20,
        )
        self.value = value
        self.sprite = pygame.image.load(
            "assets/items/exp_orb.jpg"
        ).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (20, 20))

    def apply(self, player):
        player.add_experience(self.value)

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)
