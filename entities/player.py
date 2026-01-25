from entities.entity import Entity
from settings import *


class Player(Entity):
    """Класс игрока"""

    def __init__(self, x, y):
        self.radius = 10  # Радиус вместо ширины/высоты
        super().__init__(
            x - self.radius,
            y - self.radius,
            self.radius * 2,
            self.radius * 2,
            BLUE,
        )
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.experience = 0
        self.level = 1
        self.base_damage = 3
        self.damage_multiplier = 1.0
        self.weapons = []
        self.upgrades = []
        self.last_shot_time = 0
        self.shoot_cooldown = 500  # ms

        # Флаг для ожидания выбора улучшения
        self.waiting_for_upgrade = False

    def update(self, game):
        """Обновление игрока"""
        # Если ждем выбора улучшения - не обновляем движение
        if not self.waiting_for_upgrade:
            self.handle_input()

        self.update_weapons(game)
        self.check_level_up(game)

    def draw(self, screen):
        """Отрисовка игрока"""
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

        # Отрисовка оружия
        for weapon in self.weapons:
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
        for weapon in self.weapons:
            weapon.update(game)

    def add_weapon(self, weapon):
        """Добавление оружия"""
        weapon.owner = self
        self.weapons.append(weapon)

    def add_upgrade(self, upgrade):
        """Добавление улучшения"""
        upgrade.apply(self)
        self.upgrades.append(upgrade)

    def take_damage(self, amount):
        """Получение урона"""
        self.health -= amount
        if self.health <= 0:
            self.destroy()
            return True
        return False

    def add_experience(self, amount):
        """Добавление опыта"""
        self.experience += amount

    def check_level_up(self, game):
        """Проверка повышения уровня"""
        if self.level in LEVELS:
            level_info = LEVELS[self.level]
            if (
                self.experience >= level_info["exp_required"]
                and not self.waiting_for_upgrade
                and not game.game_paused
            ):
                self.level_up(game)

    def level_up(self, game):
        """Повышение уровня"""
        exp_needed = LEVELS.get(self.level, {"exp_required": 9999})[
            "exp_required"
        ]
        self.experience -= exp_needed
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.waiting_for_upgrade = True
        print(f"Уровень повышен! Текущий уровень: {self.level}")

        # Запрашиваем меню улучшений у игры
        game.request_upgrade_menu()

    def complete_level_up(self):
        """Завершение повышения уровня"""
        self.waiting_for_upgrade = False

    def get_damage(self):
        """Получение урона с учетом множителей"""
        return self.base_damage * self.damage_multiplier
