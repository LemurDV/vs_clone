import pygame

from entities.entity import Entity
from settings import (
    BASE_EXPERIENCE,
    BLUE,
    EXPERIENCE_MULTIPLIER,
    GREEN,
    MAGNET_RADIUS,
    PLAYER_HEALTH,
    PLAYER_SPEED,
    RED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Player(Entity):
    def __init__(self, x, y):
        self.radius = 19
        super().__init__(
            x - self.radius,
            y - self.radius,
            self.radius * 2,
            self.radius * 2,
            BLUE,
        )
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.hp_regen = 0
        self.last_regent_time = 0
        self.coins = 0
        self.experience = 0
        self.experience_needed = BASE_EXPERIENCE
        self.experience_multiplier = EXPERIENCE_MULTIPLIER
        self.level = 1
        self.base_damage = 6
        self.magnet_radius = 500
        self.exp_boost = 1
        self.damage_multiplier = 1.0
        self.weapons = {}
        self.upgrades = []
        self.elements = []
        self.sprite = pygame.image.load(
            "assets/characters/wizard.jpg"
        ).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (40, 50))

        # Флаг для ожидания выбора улучшения
        self.waiting_for_upgrade = False

    def update(self, game):
        """Обновление игрока"""
        # Если ждем выбора улучшения - не обновляем движение
        if not self.waiting_for_upgrade:
            self.handle_input()

        self.update_weapons(game)
        self.update_statuses(game)
        self.check_level_up(game)

    def draw(self, screen):
        """Отрисовка игрока"""
        screen.blit(self.sprite, self.rect)
        # pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

        # Отрисовка оружия
        for weapon in self.weapons.values():
            weapon.draw(screen)
        # Отрисовка здоровья
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        """Отрисовка полоски здоровья"""
        bar_width = 50
        bar_height = 5
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 10

        # Фон полоски
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # Здоровье
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(
            screen, GREEN, (bar_x, bar_y, health_width, bar_height)
        )

    def handle_input(self):
        """Обработка ввода игрока"""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed

        # Нормализация диагонального движения
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/√2
            dy *= 0.7071

        self.move(dx, dy)

        # Ограничение движения в пределах экрана
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))

    def update_weapons(self, game):
        """Обновление оружия"""
        for weapon in self.weapons.values():
            weapon.update(game)

    def update_statuses(self, game):
        if self.hp_regen:
            self.hp_regenerate(game.particle_system)

    def add_weapon(self, weapon):
        """Добавление оружия"""
        weapon.owner = self
        self.weapons.update({weapon.name: weapon})

    def add_upgrade(self, upgrade):
        """Добавление улучшения"""
        upgrade.apply(self)
        self.upgrades.append(upgrade)

    def add_element(self, element):
        self.elements.append(element)

    def take_damage(self, amount):
        """Получение урона"""
        self.health -= amount
        if self.health <= 0:
            self.destroy()
            return True
        return False

    def add_experience(self, amount):
        """Добавление опыта"""
        self.experience += int(amount * self.exp_boost)

    def add_coin(self, value: int):
        self.coins += value

    def heal(self, amount: int):
        if self.health + amount > self.max_health:
            self.health = self.max_health
        self.health += amount

    def check_level_up(self, game):
        """Проверка повышения уровня"""
        if (
            self.experience >= self.experience_needed
            and not self.waiting_for_upgrade
            and not game.game_paused
        ):
            self.level_up(game)

    def level_up(self, game):
        """Повышение уровня"""
        self.level += 1
        if self.level % 5 == 0:
            self.experience_multiplier += 0.5
        self.experience = 0
        self.experience_needed = int(
            self.experience_needed * self.experience_multiplier
        )
        self.max_health += 10
        self.health = self.max_health
        self.waiting_for_upgrade = True
        print(f"Уровень повышен! Текущий уровень: {self.level}")

        # Запрашиваем меню улучшений у игры
        game.request_upgrade_menu()

    def hp_regenerate(self, particle_system):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_regent_time > 5_000:
            self.last_regent_time = pygame.time.get_ticks()
            self.heal(self.hp_regen)
            particle_system.add_heal_text(
                x=self.x, y=self.y, heal=self.hp_regen
            )

    def complete_level_up(self):
        """Завершение повышения уровня"""
        self.waiting_for_upgrade = False

    def get_damage(self):
        """Получение урона с учетом множителей"""
        return self.base_damage * self.damage_multiplier

    def increase_damage(self, value: int):
        self.base_damage = self.base_damage + value

    def increase_magnet_radius(self, value: int):
        self.magnet_radius += value

    def increase_exp_boost(self, value: int):
        self.exp_boost += value

    def increase_hp_regeneration(self, value: int):
        self.hp_regen += value
