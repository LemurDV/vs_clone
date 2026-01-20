# game.py
import pygame
import random
from config import *
from player import Player
from enemy import Enemy
from experience import Experience
from ui import *


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vampire Survivors Clone")

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.show_level_up = False
        self.level_up_timer = 0

        self.reset_game()

    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.enemies = []
        self.experience_orbs = []

        self.wave = 1
        self.enemies_in_wave = INITIAL_ENEMIES_PER_WAVE
        self.enemies_spawned = 0
        self.enemies_defeated = 0
        self.wave_complete = False

        self.last_enemy_spawn = 0
        self.enemy_spawn_delay = ENEMY_SPAWN_DELAY

        self.game_over = False
        self.show_level_up = False

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.game_over and event.key == pygame.K_r:
                    self.reset_game()
                if event.key == pygame.K_SPACE and not self.game_over:
                    # Быстрая стрельба при нажатии пробела (для тестирования)
                    self.player.shoot(pygame.time.get_ticks())

    def spawn_enemies(self, current_time):
        """Спавн врагов"""
        if (current_time - self.last_enemy_spawn > self.enemy_spawn_delay and
                self.enemies_spawned < self.enemies_in_wave and
                len(self.enemies) < MAX_ENEMIES_ON_SCREEN):
            self.enemies.append(Enemy())
            self.last_enemy_spawn = current_time
            self.enemies_spawned += 1

    def update_wave(self):
        """Обновление состояния волны"""
        # Проверка завершения волны
        if self.enemies_spawned >= self.enemies_in_wave and len(
                self.enemies) == 0:
            if not self.wave_complete:
                self.wave_complete = True
                # Награда за волну
                self.player.add_exp(WAVE_REWARD_EXP)
            else:
                # Переход к следующей волне
                self.wave += 1
                self.enemies_in_wave = INITIAL_ENEMIES_PER_WAVE + self.wave * ENEMY_INCREASE_PER_WAVE
                self.enemies_spawned = 0
                self.enemies_defeated = 0
                self.wave_complete = False
                # Уменьшение задержки спавна врагов
                self.enemy_spawn_delay = max(
                    MIN_ENEMY_SPAWN_DELAY,
                    ENEMY_SPAWN_DELAY - self.wave * ENEMY_SPAWN_DELAY_DECREASE
                )

    def check_collisions(self):
        """Проверка всех столкновений"""
        # Проверка столкновений врагов с игроком
        for enemy in self.enemies[:]:
            if enemy.check_collision_with_player(self.player.x, self.player.y,
                                                 self.player.radius):
                self.player.take_damage(5)
                self.enemies.remove(enemy)
                if not self.player.is_alive:
                    self.game_over = True

        # Проверка столкновений снарядов с врагами
        for projectile in self.player.projectiles[:]:
            for enemy in self.enemies[:]:
                if projectile.check_collision(enemy.x, enemy.y, enemy.radius):
                    if not enemy.take_damage(projectile.damage):
                        # Враг умер
                        self.experience_orbs.append(
                            Experience(enemy.x, enemy.y, enemy.exp_value)
                        )
                        self.enemies.remove(enemy)
                        self.enemies_defeated += 1

                    if projectile in self.player.projectiles:
                        self.player.projectiles.remove(projectile)
                    break

        # Проверка сбора опыта
        for exp_orb in self.experience_orbs[:]:
            if exp_orb.check_collection(self.player.x, self.player.y,
                                        self.player.radius):
                if self.player.add_exp(exp_orb.value):
                    self.show_level_up = True
                    self.level_up_timer = pygame.time.get_ticks()
                self.experience_orbs.remove(exp_orb)

        # Удаление врагов за пределами экрана
        for enemy in self.enemies[:]:
            if enemy.is_off_screen():
                self.enemies.remove(enemy)

    def update_level_up_message(self, current_time):
        """Обновление таймера сообщения о повышении уровня"""
        if self.show_level_up and current_time - self.level_up_timer > 2000:  # 2 секунды
            self.show_level_up = False

    def draw(self):
        """Отрисовка всех элементов игры"""
        self.screen.fill(BLACK)

        # Отрисовка опыта
        for exp_orb in self.experience_orbs:
            exp_orb.draw(self.screen)

        # Отрисовка снарядов
        for projectile in self.player.projectiles:
            projectile.draw(self.screen)

        # Отрисовка врагов
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Отрисовка игрока
        if self.player.is_alive:
            self.player.draw(self.screen)

        # Подготовка данных для интерфейса
        player_stats = self.player.get_stats()
        wave_info = {
            'current_wave': self.wave,
            'enemies_remaining': self.enemies_in_wave - self.enemies_defeated,
            'total_enemies': self.enemies_in_wave
        }

        # Отрисовка интерфейса
        draw_hud(self.screen, player_stats, wave_info, self.show_level_up)

        # Отрисовка сообщения о завершении волны
        if self.wave_complete and not self.game_over:
            draw_wave_complete(self.screen, self.wave - 1)

        # Отрисовка экрана окончания игры
        if self.game_over:
            draw_game_over(self.screen, player_stats, wave_info)

        pygame.display.flip()

    def run(self):
        """Главный игровой цикл"""
        while self.running:
            current_time = pygame.time.get_ticks()

            self.handle_events()

            if self.game_over:
                self.draw()
                self.clock.tick(FPS)
                continue

            # Управление игроком
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.player.shoot(current_time)

            # Обновление снарядов
            self.player.update_projectiles()

            # Спавн врагов
            self.spawn_enemies(current_time)

            # Обновление волны
            self.update_wave()

            # Движение врагов к игроку
            for enemy in self.enemies:
                enemy.move(self.player.x, self.player.y)

            # Движение опыта к игроку
            for exp_orb in self.experience_orbs:
                exp_orb.move(self.player.x, self.player.y)

            # Проверка столкновений
            self.check_collisions()

            # Обновление сообщения о повышении уровня
            self.update_level_up_message(current_time)

            # Отрисовка
            self.draw()

            self.clock.tick(FPS)

        pygame.quit()