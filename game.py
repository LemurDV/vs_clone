from loguru import logger

from config import (
    BLACK,
    ENEMY_INCREASE_PER_WAVE,
    ENEMY_SPAWN_DELAY,
    ENEMY_SPAWN_DELAY_DECREASE,
    FPS,
    HEIGHT,
    INITIAL_ENEMIES_PER_WAVE,
    MAX_ENEMIES_ON_SCREEN,
    MIN_ENEMY_SPAWN_DELAY,
    RED,
    WAVE_REWARD_EXP,
    WHITE,
    WIDTH,
    pygame,
)
from damage_text import DamageText
from enemy import Enemy
from experience import Experience
from player import Player
from ui import draw_game_over, draw_hud, draw_wave_complete
from upgrade_screen import UpgradeScreen


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vampire Survivors Clone")

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.paused = False
        self.show_level_up = False
        self.level_up_timer = 0

        self.damage_texts = []

        # Для экрана улучшений
        self.upgrade_screen = None
        self.choosing_upgrade = False

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
        self.paused = False
        self.choosing_upgrade = False
        self.upgrade_screen = None

        # Статистика
        self.total_damage_dealt = 0
        self.total_enemies_killed = 0
        self.total_exp_collected = 0

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

                if (
                    event.key == pygame.K_SPACE
                    and not self.game_over
                    and not self.choosing_upgrade
                ):
                    # Быстрая стрельба при нажатии пробела
                    self.player.shoot(pygame.time.get_ticks())

                if (
                    event.key == pygame.K_p
                    and not self.game_over
                    and not self.choosing_upgrade
                ):
                    # Пауза
                    self.paused = not self.paused

            # Передача событий на экран улучшений
            if self.choosing_upgrade and self.upgrade_screen:
                if self.upgrade_screen.handle_event(event):
                    # Игрок выбрал улучшение
                    self.apply_selected_upgrade()

    def apply_selected_upgrade(self):
        """Применение выбранного улучшения"""
        if self.upgrade_screen.selected_upgrade:
            upgrade_type = self.upgrade_screen.selected_upgrade
            self.player.apply_upgrade(upgrade_type)

            # Завершаем повышение уровня
            self.player.apply_level_up()

            # Выходим из режима выбора улучшений
            self.choosing_upgrade = False
            self.upgrade_screen = None
            self.paused = False

            # Показываем сообщение о выбранном улучшении
            self.show_level_up = True
            self.level_up_timer = pygame.time.get_ticks()

    def spawn_enemies(self, current_time):
        """Спавн врагов"""
        if (
            current_time - self.last_enemy_spawn > self.enemy_spawn_delay
            and self.enemies_spawned < self.enemies_in_wave
            and len(self.enemies) < MAX_ENEMIES_ON_SCREEN
        ):
            self.enemies.append(Enemy())
            self.last_enemy_spawn = current_time
            self.enemies_spawned += 1

    def update_wave(self):
        """Обновление состояния волны"""
        # Проверка завершения волны
        if (
            self.enemies_spawned >= self.enemies_in_wave
            and len(self.enemies) == 0
        ):
            if not self.wave_complete:
                self.wave_complete = True
                # Награда за волну
                exp_gained = self.player.add_exp(WAVE_REWARD_EXP)
                self.total_exp_collected += WAVE_REWARD_EXP
                if exp_gained:
                    self.show_upgrade_screen()
            else:
                # Переход к следующей волне
                self.wave += 1
                self.enemies_in_wave = (
                    INITIAL_ENEMIES_PER_WAVE
                    + self.wave * ENEMY_INCREASE_PER_WAVE
                )
                self.enemies_spawned = 0
                self.enemies_defeated = 0
                self.wave_complete = False
                # Уменьшение задержки спавна врагов
                self.enemy_spawn_delay = max(
                    MIN_ENEMY_SPAWN_DELAY,
                    ENEMY_SPAWN_DELAY - self.wave * ENEMY_SPAWN_DELAY_DECREASE,
                )

    def show_upgrade_screen(self):
        """Показать экран выбора улучшений"""
        self.choosing_upgrade = True
        self.paused = True
        self.upgrade_screen = UpgradeScreen(self.player)

    def check_collisions(self):
        """Проверка всех столкновений"""
        # Проверка столкновений врагов с игроком
        for enemy in self.enemies[:]:
            if enemy.check_collision_with_player(
                self.player.x, self.player.y, self.player.radius
            ):
                self.player.take_damage(5)
                self.enemies.remove(enemy)
                if not self.player.is_alive:
                    self.game_over = True

        # Проверка столкновений снарядов с врагами
        for projectile in self.player.projectiles[:]:
            for enemy in self.enemies[:]:
                if projectile.check_collision(enemy.x, enemy.y, enemy.radius):
                    damage_dealt = projectile.damage
                    alive, actual_damage = enemy.take_damage(
                        damage_dealt,
                        # projectile.color,
                    )

                    self.damage_texts.append(
                        DamageText(
                            enemy.x,
                            enemy.y - enemy.radius - 10,
                            damage_dealt,
                            projectile.color,
                        )
                    )

                    if not alive:
                        self.experience_orbs.append(
                            Experience(enemy.x, enemy.y, enemy.exp_value)
                        )
                        self.enemies.remove(enemy)
                        self.enemies_defeated += 1
                        self.total_enemies_killed += 1

                        # Статистика урона
                        self.total_damage_dealt += damage_dealt

                        # Вампиризм
                        self.player.apply_vampirism(damage_dealt)

                    if projectile in self.player.projectiles:
                        self.player.projectiles.remove(projectile)
                    break  # Важно: снаряд поражает только одного врага

    def update_level_up_message(self, current_time):
        """Обновление таймера сообщения о повышении уровня"""
        if self.show_level_up and current_time - self.level_up_timer > 1500:
            self.show_level_up = False

    def draw(self):
        """Отрисовка всех элементов игры"""
        self.screen.fill(BLACK)

        # Отрисовка опыта
        for exp_orb in self.experience_orbs:
            exp_orb.draw(self.screen)

        self.player.draw_weapons(self.screen)

        # Отрисовка снарядов
        for projectile in self.player.projectiles:
            projectile.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for damage_text in self.damage_texts:
            damage_text.draw(self.screen)

        # Отрисовка игрока
        if self.player.is_alive:
            self.player.draw(self.screen)

        # Подготовка данных для интерфейса
        player_stats = self.player.get_stats()
        wave_info = {
            "current_wave": self.wave,
            "enemies_remaining": self.enemies_in_wave - self.enemies_defeated,
            "total_enemies": self.enemies_in_wave,
        }

        # Отрисовка интерфейса
        draw_hud(self.screen, player_stats, wave_info, self.show_level_up)

        # Отрисовка сообщения о завершении волны
        # if (
        #     self.wave_complete
        #     and not self.game_over
        #     and not self.choosing_upgrade
        # ):
        #     draw_wave_complete(self.screen, self.wave - 1)

        # Отрисовка экрана выбора улучшений
        if self.choosing_upgrade and self.upgrade_screen:
            self.upgrade_screen.draw(self.screen)

        # Отрисовка паузы
        elif self.paused and not self.choosing_upgrade:
            self.draw_pause_screen()

        # Отрисовка экрана окончания игры
        if self.game_over:
            draw_game_over(self.screen, player_stats, wave_info)

        pygame.display.flip()

    def draw_pause_screen(self):
        """Отрисовка экрана паузы"""
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 72)
        text = font.render("ПАУЗА", True, WHITE)
        self.screen.blit(
            text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50)
        )

        small_font = pygame.font.Font(None, 36)
        hint = small_font.render(
            "Нажмите P для продолжения", True, (200, 200, 200)
        )
        self.screen.blit(
            hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 30)
        )

    def run(self):
        """Главный игровой цикл"""
        while self.running:
            current_time = pygame.time.get_ticks()

            self.handle_events()
            self.player.update_weapons(current_time, self.enemies)

            if self.game_over or self.paused:
                # Если игра на паузе или окончена, только рисуем и ждем
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
            for enemy in self.enemies[:]:
                enemy.move(self.player.x, self.player.y)

            # Движение опыта к игроку
            for exp_orb in self.experience_orbs:
                exp_orb.move(self.player.x, self.player.y)

            # Проверка столкновений
            self.check_collisions()

            for enemy in self.enemies[:]:
                if not enemy.is_alive:
                    self.experience_orbs.append(
                        Experience(enemy.x, enemy.y, enemy.exp_value)
                    )
                    self.enemies.remove(enemy)
                    self.enemies_defeated += 1
                    self.total_enemies_killed += 1

            for damage_text in self.damage_texts[:]:
                if not damage_text.update():
                    self.damage_texts.remove(damage_text)

            self.update_level_up_message(current_time)

            self.draw()

            self.clock.tick(FPS)
