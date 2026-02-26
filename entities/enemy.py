import pygame

from entities.entity import Entity
from settings import (
    ENEMY_SPEED,
    GREEN,
    RED,
)
from systems.effect_manager import StatusEffect


class Enemy(Entity):
    """Базовый класс врага"""

    def __init__(
        self,
        x,
        y,
        width,
        height,
        color,
        health,
        damage,
        experience_value,
        sprite_path,
    ):
        super().__init__(x, y, width, height, color)
        self.health = health
        self.max_health = health
        self.damage = damage
        self.experience_value = experience_value
        self.speed = ENEMY_SPEED
        self.last_attack_time = 0
        self.attack_cooldown = 1000  # ms
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.is_bleeding = False
        self.last_bleed_time = 0
        self.active_effects = {}

    def update(self, game):
        """Обновление врага"""
        if not self.active:
            return

        self.update_statuses(game)

        # Движение к игроку
        player = game.player
        if player and player.active:
            dx = player.rect.centerx - (self.x + self.rect.width / 2)
            dy = player.rect.centery - (self.y + self.rect.height / 2)

            # Нормализация направления
            distance = max(0.1, (dx**2 + dy**2) ** 0.5)
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed

            self.move(dx, dy)

            # Проверка атаки
            if self.check_collision(player):
                self.attack(player)

    def apply_effect(self, effect: StatusEffect) -> None:
        effect.start_time = pygame.time.get_ticks()

        existing_effect: StatusEffect = self.active_effects.get(
            effect.effect_type
        )

        if existing_effect:
            if (
                existing_effect.current_stack_count
                == existing_effect.max_stack_count
            ):
                pass
            else:
                existing_effect.current_stack_count += 1
                existing_effect.damage_per_tick = min(
                    existing_effect.damage_per_tick
                    * existing_effect.current_stack_count,
                    effect.max_damage_per_tick,
                )
            existing_effect.duration = effect.duration
        else:
            self.active_effects.update({effect.effect_type: effect})

    def update_statuses(self, game):
        if not self.active_effects:
            return

        current_time = pygame.time.get_ticks()

        for effect_type in list(self.active_effects.keys()):
            effect = self.active_effects[effect_type]

            if current_time - effect.start_time > effect.duration:
                self.active_effects.pop(effect_type)
                continue

            if current_time - effect.last_tick_time > effect.tick_interval:
                effect.last_tick_time = current_time
                self.take_damage(
                    amount=effect.damage_per_tick,
                    game=game,
                    color=effect.color,
                )

    def draw(self, screen):
        """Отрисовка врага"""
        screen.blit(self.sprite, self.rect)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        """Отрисовка полоски здоровья"""
        if self.health < self.max_health:
            bar_width = self.rect.width
            bar_height = 3
            bar_x = self.rect.x
            bar_y = self.rect.y - 5

            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            health_width = (self.health / self.max_health) * bar_width
            pygame.draw.rect(
                screen, GREEN, (bar_x, bar_y, health_width, bar_height)
            )

    def attack(self, player):
        """Атака игрока"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            player.take_damage(self.damage)
            self.last_attack_time = current_time

    def take_damage(self, amount, game, is_critical=False, color=RED):
        """Получение урона"""
        self.health -= amount

        game.particle_system.add_damage_text(
            self.rect.centerx,
            self.rect.top - 15,
            int(amount),
            color,
            is_critical,
        )

        if self.health <= 0:
            if game:
                game.enemy_died(self)
            self.destroy()
            return True
        return False
