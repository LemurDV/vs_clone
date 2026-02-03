import pygame

from entities.player import Player
from loot.loot_manager import LootManager
from settings import (
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SPAWN_RATE,
)
from systems.collision_system import CollisionSystem
from systems.enemy_manager import EnemyManager
from systems.particle_system import ParticleSystem
from ui.base_hud import BaseHud
from ui.upgrade_menu import UpgradeMenu
from upgrades.upgrade_manager import UpgradeManager
from weapons.aura_weapon import AuraWeapon
from weapons.magic_bullet_weapon import MagicBulletWeapon


class Game:
    """Основной класс игры"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load("assets/maps/map_1.png")
        self.background = pygame.transform.scale(
            self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 24)

        # Игровые объекты
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.experience_orbs = []

        # Лут и предметы
        self.loot_items = []  # TODO: добавить лут систему или манагера?

        # Время
        self.start_time = pygame.time.get_ticks()
        self.last_spawn_time = 0
        self.game_time = 0
        self.last_key_press_time = 0

        # Статистика
        self.enemies_killed = 0
        self.coins_collected = 0

        # Флаг для паузы при выборе улучшений
        self.game_paused = False

        # Системы
        self.enemy_manager = EnemyManager()
        self.collision_system = CollisionSystem(self)
        self.upgrade_manager = UpgradeManager()
        self.upgrade_menu = UpgradeMenu(self)
        self.particle_system = ParticleSystem()
        self.loot_manager = LootManager()
        self.hud = BaseHud(self)

        # Инициализация
        self.init_game()

    def init_game(self):
        """Инициализация игры"""
        # Добавляем стартовое оружие
        # start_weapon = MagicBulletWeapon()
        start_weapon = AuraWeapon()
        self.player.add_weapon(start_weapon)

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

    def add_loot_item(self, item):
        """Добавить предмет лута в мир"""
        self.loot_items.append(item)

    def enemy_died(self, enemy):
        """Вызывается при смерти врага"""
        # Вызываем дроп через менеджер
        self.loot_manager.drop_from_enemy(enemy, self)
        self.enemies_killed += 1

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
            self.collision_system.update()

        # Обновление врагов
        # for enemy in self.enemies[:]:
        for enemy in self.enemy_manager.enemies:
            if enemy.active:
                enemy.update(self)
            else:
                # Враг умер - удаляем из списка
                self.enemy_manager.enemies.remove(enemy)
                # enemy_died уже вызван в take_damage, так что не вызываем здесь

        # Обновление сфер опыта
        for orb in self.experience_orbs[:]:
            if orb.active:
                orb.update(self)
            else:
                self.experience_orbs.remove(orb)

        # Обновление предметов лута
        for loot in self.loot_items[:]:
            loot.update(self)
            if not loot.active:
                self.loot_items.remove(loot)

        # Обновление системы частиц
        self.particle_system.update()

        # Спавн новых врагов
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > SPAWN_RATE:
            self.enemy_manager.spawn_enemy(current_level=self.player.level)
            self.last_spawn_time = current_time

    def draw(self):
        """Отрисовка игры"""
        self.screen.blit(self.background, (0, 0))

        # Отрисовка сфер опыта
        for orb in self.experience_orbs:
            orb.draw(self.screen)

        # Отрисовка предметов лута
        for loot in self.loot_items:
            loot.draw(self.screen)

        # Отрисовка врагов
        for enemy in self.enemy_manager.enemies:
            enemy.draw(self.screen)

        # Отрисовка игрока
        if self.player.active:
            self.player.draw(self.screen)

        # Отрисовка частиц (тексты урона и эффекты)
        self.particle_system.draw(self.screen)

        # Отрисовка интерфейса
        self.hud.draw_ui()

        # Отрисовка меню улучшений (если активно, поверх всего)
        self.upgrade_menu.draw(self.screen)

        pygame.display.flip()
