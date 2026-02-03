import pygame

from entities.entity import Entity
from settings import (
    ENEMY_SPEED,
    GREEN,
    RED,
)


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

    def update_statuses(self, game):
        if self.is_bleeding and self.time_to_bleed():
            self.last_bleed_time = pygame.time.get_ticks()
            self.take_damage(1, game)

    def time_to_bleed(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_bleed_time > 2_000

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

    def take_damage(self, amount, game, is_critical=False):
        """Получение урона"""
        self.health -= amount

        # Создаем текст урона через систему частиц
        game.particle_system.add_damage_text(
            self.rect.centerx,
            self.rect.top - 15,
            int(amount),
            RED,
            is_critical,
        )

        if self.health <= 0:
            # Вызываем смерть врага через игру
            if game:
                game.enemy_died(self)
            self.destroy()
            return True
        return False
