from entities.damage_text import DamageText
from entities.entity import Entity
from entities.experience_orb import ExperienceOrb
from settings import *


class Enemy(Entity):
    """Базовый класс врага"""

    def __init__(
        self, x, y, width, height, color, health, damage, experience_value
    ):
        super().__init__(x, y, width, height, color)
        self.health = health
        self.max_health = health
        self.damage = damage
        self.experience_value = experience_value
        self.speed = ENEMY_SPEED
        self.last_attack_time = 0
        self.attack_cooldown = 1000  # ms

    def update(self, game):
        """Обновление врага"""
        if not self.active:
            return

        # Движение к игроку
        player = game.player
        if player and player.active:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery

            # Нормализация направления
            distance = max(0.1, (dx**2 + dy**2) ** 0.5)
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed

            self.move(dx, dy)

            # Проверка атаки
            if self.check_collision(player):
                self.attack(player)

    def draw(self, screen):
        """Отрисовка врага"""
        pygame.draw.rect(screen, self.color, self.rect)

        # Отрисовка здоровья
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

    def take_damage(self, amount, game=None, is_critical=False):
        """Получение урона"""
        self.health -= amount

        # Создаем текст урона через систему частиц
        if game and game.particle_system:
            game.particle_system.add_damage_text(
                self.rect.centerx,
                self.rect.top - 15,  # Чуть выше
                int(amount),
                RED if is_critical else (RED if amount >= 10 else ORANGE),
                is_critical,
            )

        if self.health <= 0:
            # Сохраняем позицию перед уничтожением
            x, y = self.rect.centerx, self.rect.centery
            exp_value = self.experience_value
            self.destroy()

            # Создаем сферу опыта
            if game:
                game.spawn_experience_orb(x, y, exp_value)
            return True
        return False

    def die(self):
        """Смерть врага"""
        self.destroy()
        return self.experience_value
