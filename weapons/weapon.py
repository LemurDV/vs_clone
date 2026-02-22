from abc import ABC, abstractmethod

import pygame

from entities import Enemy


class Weapon(ABC):
    def __init__(
        self,
        name: str,
        name_ui: str,
        damage: int,
        cooldown: int,
        weapon_type,
        causes_bleeding_chance: float = 0.0,
        causes_burn_chance: float = 0.0,
        causes_poison_chance: float = 0.0,
    ):
        self.name = name
        self.name_ui = name_ui
        self.damage = damage
        self.cooldown = cooldown  # ms
        self.causes_bleeding_chance: float = causes_bleeding_chance
        self.bleed_damage: int = 1
        self.causes_burn_chance: float = causes_burn_chance
        self.burn_damage: int = 1
        self.causes_poison_chance: float = causes_poison_chance
        self.poison_damage: int = 1
        self.last_attack_time = 0
        self.owner = None
        self.level = 1
        self.max_level = 5
        self.weapon_type = weapon_type  # TODO сделать enum
        self.hit_enemies = []
        self.len_hit_enemies = 0

    @abstractmethod
    def update(self, game):
        """Обновление оружия"""
        pass

    def add_enemy_to_hit(self, enemy: Enemy) -> None:
        self.hit_enemies.append(enemy)
        self.len_hit_enemies = len(set(self.hit_enemies))

    def is_collision(self, enemy) -> bool:
        pass

    def detect_enemies_in_range(self, enemies: list[Enemy], direction):
        pass

    def action_after_deal_damage(self):
        self.last_attack_time = pygame.time.get_ticks()

    def reset_hit_enemies(self):
        self.hit_enemies = []
        self.len_hit_enemies = 0

    def remove_enemy_from_list(self, enemy: Enemy):
        if enemy in self.hit_enemies:
            self.hit_enemies.remove(enemy)
            self.len_hit_enemies -= 1

    def get_damage(self):
        return self.damage + self.owner.get_damage() // 2

    @abstractmethod
    def draw(self, screen):
        """Отрисовка оружия"""
        pass

    def can_attack(self):
        """Проверка возможности атаки"""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_attack_time > self.cooldown

    def level_up(self):
        """Улучшение оружия"""
        pass
