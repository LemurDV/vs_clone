import random

import pygame

from entities import BatEnemy, SlimeEnemy
from entities.enemy import *
from entities.player import Player
from settings import *
from ui.upgrade_menu import UpgradeMenu
from upgrades.damage_upgrade import DamageUpgrade
from upgrades.new_weapon_upgrade import NewWeaponUpgrade
from upgrades.upgrade_manager import UpgradeManager
from weapons.aura_weapon import AuraWeapon
from weapons.magic_bullet_weapon import MagicBulletWeapon


class Game:
    """Основной класс игры"""

    def __init__(self):
        self.screen = SCREEN
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 24)

        # Игровые объекты
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = []
        self.experience_orbs = []

        # Системы
        self.upgrade_manager = UpgradeManager()
        self.upgrade_menu = UpgradeMenu(self)

        # Время
        self.start_time = pygame.time.get_ticks()
        self.last_spawn_time = 0
        self.game_time = 0
        self.last_key_press_time = 0  # Для предотвращения множественных нажатий

        # Статистика
        self.enemies_killed = 0

        # Флаг для паузы при выборе улучшений
        self.game_paused = False

        # Инициализация
        self.init_game()

    def init_game(self):
        """Инициализация игры"""
        # Добавляем стартовое оружие
        aura = AuraWeapon()
        self.player.add_weapon(aura)

        # Добавляем оружие в пул улучшений
        self.upgrade_manager.add_new_upgrade(
            NewWeaponUpgrade(MagicBulletWeapon)
        )
        self.upgrade_manager.add_new_upgrade(NewWeaponUpgrade(AuraWeapon))

        # Создаем тестовых врагов
        self.create_enemies()

    def request_upgrade_menu(self):
        """Запрос на показ меню улучшений"""
        self.game_paused = True
        random_upgrades = self.upgrade_manager.get_random_upgrades(
            3, self.player
        )
        self.upgrade_menu.show(random_upgrades)

    def on_upgrade_selected(self):
        """Вызывается после выбора улучшения"""
        self.player.complete_level_up()
        self.game_paused = False

    def create_enemies(self):
        """Создание врагов"""
        for _ in range(5):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            enemy = SlimeEnemy(x, y)
            self.enemies.append(enemy)

    def spawn_enemy(self):
        """Создание нового врага"""
        # Ограничение по количеству врагов в зависимости от уровня
        max_enemies = LEVELS.get(self.player.level, {"max_enemies": 20})[
            "max_enemies"
        ]
        if len(self.enemies) >= max_enemies:
            return

        side = random.randint(0, 3)
        if side == 0:  # Сверху
            x = random.randint(0, SCREEN_WIDTH)
            y = -20
        elif side == 1:  # Справа
            x = SCREEN_WIDTH + 20
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # Снизу
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 20
        else:  # Слева
            x = -20
            y = random.randint(0, SCREEN_HEIGHT)

        if random.random() < 0.5:
            enemy = SlimeEnemy(x, y)
        else:
            enemy = BatEnemy(x, y)

        self.enemies.append(enemy)

    def spawn_experience_orb(self, x, y, value):
        """Создание сферы опыта"""
        orb = ExperienceOrb(x, y, value)
        self.experience_orbs.append(orb)

    def run(self):
        """Запуск основного цикла игры"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # Передаем нажатия клавиш в меню улучшений
                if self.game_paused and self.upgrade_menu.active:
                    self.upgrade_menu.handle_keydown(event.key)

            # Передаем события мыши в меню улучшений
            elif self.game_paused and self.upgrade_menu.active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.upgrade_menu.handle_mouse_click(
                        event.pos, event.button
                    )
                elif event.type == pygame.MOUSEMOTION:
                    self.upgrade_menu.handle_mouse_motion(event.pos)

    def update(self):
        """Обновление игры"""
        self.game_time = pygame.time.get_ticks() - self.start_time

        # Если игра на паузе (показ меню улучшений), не обновляем игровую логику
        if self.game_paused:
            return

        # Обновление игрока
        if self.player.active:
            self.player.update(self)

        # Обновление врагов
        for enemy in self.enemies[:]:
            if enemy.active:
                enemy.update(self)
            else:
                self.enemies.remove(enemy)
                self.enemies_killed += 1

        # Обновление сфер опыта
        for orb in self.experience_orbs[:]:
            if orb.active:
                orb.update(self)
            else:
                self.experience_orbs.remove(orb)

        # Спавн новых врагов
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > SPAWN_RATE:
            self.spawn_enemy()
            self.last_spawn_time = current_time

    def draw(self):
        """Отрисовка игры"""
        self.screen.fill(BLACK)

        # Отрисовка сфер опыта
        for orb in self.experience_orbs:
            orb.draw(self.screen)

        # Отрисовка врагов
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Отрисовка игрока
        if self.player.active:
            self.player.draw(self.screen)

        # Отрисовка интерфейса
        self.draw_ui()

        # Отрисовка меню улучшений (если активно, поверх всего)
        self.upgrade_menu.draw(self.screen)

        pygame.display.flip()

    def draw_ui(self):
        """Отрисовка интерфейса"""
        # Здоровье
        health_text = self.font.render(
            f"HP: {self.player.health}/{self.player.max_health}", True, WHITE
        )
        self.screen.blit(health_text, (10, 10))

        # Уровень и опыт
        exp_needed = LEVELS.get(self.player.level, {"exp_required": 9999})[
            "exp_required"
        ]
        exp_text = self.font.render(
            f"Уровень: {self.player.level} | Опыт: {self.player.experience}/{exp_needed}",
            True,
            WHITE,
        )
        self.screen.blit(exp_text, (10, 40))

        # Враги
        enemies_text = self.font.render(
            f"Врагов: {len(self.enemies)} | Убито: {self.enemies_killed}",
            True,
            WHITE,
        )
        self.screen.blit(enemies_text, (10, 70))

        # Время
        minutes = self.game_time // 60000
        seconds = (self.game_time % 60000) // 1000
        time_text = self.font.render(
            f"Время: {minutes:02d}:{seconds:02d}", True, WHITE
        )
        self.screen.blit(time_text, (SCREEN_WIDTH - 150, 10))

        # Инструкции (только если нет меню)
        if not self.game_paused:
            controls = self.font.render(
                "WASD - движение | ESC - выход", True, WHITE
            )
            self.screen.blit(
                controls,
                (
                    SCREEN_WIDTH // 2 - controls.get_width() // 2,
                    SCREEN_HEIGHT - 30,
                ),
            )

        # Статистика по оружию
        y_pos = 100
        for weapon in self.player.weapons:
            weapon_text = self.font.render(
                f"{weapon.name} (Ур. {weapon.level})", True, WHITE
            )
            self.screen.blit(weapon_text, (10, y_pos))
            y_pos += 25

        # Индикатор паузы (если меню активно)
        if self.game_paused:
            pause_text = self.font.render(
                "ПАУЗА: Выбор улучшения", True, YELLOW
            )
            self.screen.blit(
                pause_text,
                (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 20),
            )
