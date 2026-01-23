import math
import os
import random

from loguru import logger
import pygame

from config import (
    BLACK,
    CAMERA_SAFE_ZONE,
    ENEMY_INCREASE_PER_WAVE,
    ENEMY_MAX_RADIUS,
    ENEMY_MIN_RADIUS,
    ENEMY_SPAWN_DELAY,
    ENEMY_SPAWN_DELAY_DECREASE,
    FPS,
    HEIGHT,
    INITIAL_ENEMIES_PER_WAVE,
    MAP_PATHS,
    MAX_ENEMIES_ON_SCREEN,
    MIN_ENEMY_SPAWN_DELAY,
    PLAYER_MOVEMENT_SPEED,
    PLAYER_RADIUS,
    WAVE_REWARD_EXP,
    WHITE,
    WIDTH,
)
from damage_text import DamageText
from enemy import Enemy
from experience import Experience
from player import Player
from ui import draw_game_over, draw_hud
from upgrade_screen import UpgradeScreen


class Game:
    def __init__(self, selected_level=1):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vampire Survivors Clone")

        self.selected_level = selected_level

        # Загружаем карту для выбранного уровня
        self.map_image = self.load_map(selected_level)
        self.map_width = self.map_image.get_width()
        self.map_height = self.map_image.get_height()

        # Камера (смещение карты)
        self.camera_x = self.map_width // 2 - WIDTH // 2
        self.camera_y = self.map_height // 2 - HEIGHT // 2

        # Позиция игрока на карте (не на экране!)
        self.player_world_x = self.map_width // 2
        self.player_world_y = self.map_height // 2

        # Границы карты
        self.map_min_x = 0
        self.map_min_y = 0
        self.map_max_x = self.map_width - WIDTH
        self.map_max_y = self.map_height - HEIGHT

        # Инициализация игрока в центре экрана
        self.player = Player(WIDTH // 2, HEIGHT // 2)

        # Другие инициализации...
        self.enemies = []
        self.experience_orbs = []
        self.damage_texts = []

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.paused = False
        self.show_level_up = False
        self.level_up_timer = 0

        self.wave = 1
        self.enemies_in_wave = INITIAL_ENEMIES_PER_WAVE
        self.enemies_spawned = 0
        self.enemies_defeated = 0
        self.wave_complete = False

        self.last_enemy_spawn = 0
        self.enemy_spawn_delay = ENEMY_SPAWN_DELAY

        self.choosing_upgrade = False
        self.upgrade_screen = None

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

    def load_map(self, level):
        """Загрузка карты для указанного уровня"""
        map_path = MAP_PATHS.get(level, "assets/maps/level1_map.jpg")

        # Создаем папку assets/maps если ее нет
        os.makedirs(os.path.dirname(map_path), exist_ok=True)

        # Если файл существует, загружаем его
        if os.path.exists(map_path):
            try:
                return pygame.image.load(map_path).convert()
            except pygame.error as e:
                print(f"Не удалось загрузить карту: {map_path}, ошибка: {e}")
                # Создаем простую карту по умолчанию
                return self.create_default_map()
        else:
            print(f"Карта не найдена: {map_path}. Создаю карту по умолчанию.")
            # Создаем простую карту по умолчанию
            return self.create_default_map()

    def create_default_map(self):
        """Создание простой карты по умолчанию"""
        default_width, default_height = 3000, 3000
        map_surface = pygame.Surface((default_width, default_height))

        # Заливаем базовым цветом в зависимости от уровня
        level_colors = {
            1: (30, 30, 60),  # Темно-синий
            2: (60, 30, 30),  # Темно-красный
            3: (30, 60, 30),  # Темно-зеленый
        }

        base_color = level_colors.get(self.selected_level, (30, 30, 60))
        map_surface.fill(base_color)

        # Добавляем простую текстуру
        for i in range(0, default_width, 50):
            for j in range(0, default_height, 50):
                # Шахматный узор
                if (i // 50 + j // 50) % 2 == 0:
                    color = tuple(min(255, c + 20) for c in base_color)
                    pygame.draw.rect(map_surface, color, (i, j, 50, 50))

        return map_surface

    def update_camera(self):
        """Обновление позиции камеры - всегда центрируем на игроке"""
        # Целевая позиция камеры (чтобы игрок был в центре)
        target_camera_x = self.player_world_x - WIDTH // 2
        target_camera_y = self.player_world_y - HEIGHT // 2

        # Ограничиваем камеру границами карты
        self.camera_x = max(
            self.map_min_x, min(target_camera_x, self.map_max_x)
        )
        self.camera_y = max(
            self.map_min_y, min(target_camera_y, self.map_max_y)
        )

        # Если камера достигла границы, игрок начинает двигаться от центра
        player_offset_x = 0
        player_offset_y = 0

        # Проверяем левую границу
        if self.camera_x <= self.map_min_x:
            player_offset_x = self.player_world_x - (WIDTH // 2)
        # Проверяем правую границу
        elif self.camera_x >= self.map_max_x:
            player_offset_x = self.player_world_x - (
                self.map_width - WIDTH // 2
            )

        # Проверяем верхнюю границу
        if self.camera_y <= self.map_min_y:
            player_offset_y = self.player_world_y - (HEIGHT // 2)
        # Проверяем нижнюю границу
        elif self.camera_y >= self.map_max_y:
            player_offset_y = self.player_world_y - (
                self.map_height - HEIGHT // 2
            )

        # Возвращаем смещение игрока от центра
        return player_offset_x, player_offset_y

    def world_to_screen(self, world_x, world_y):
        """Преобразование мировых координат в экранные"""
        screen_x = world_x - self.camera_x
        screen_y = world_y - self.camera_y
        return int(screen_x), int(screen_y)

    def screen_to_world(self, screen_x, screen_y):
        """Преобразование экранных координат в мировые"""
        world_x = screen_x + self.camera_x
        world_y = screen_y + self.camera_y
        return world_x, world_y

    def get_visible_area(self):
        """Возвращает видимую область карты в мировых координатах"""
        return pygame.Rect(self.camera_x, self.camera_y, WIDTH, HEIGHT)

    def move_player(self, keys):
        """Движение игрока с плавным перемещением карты"""
        dx, dy = 0, 0
        player_movement_speed = self.player.current_movement_speed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= player_movement_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += player_movement_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= player_movement_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += player_movement_speed

        # Если есть движение, нормализуем вектор
        if dx != 0 or dy != 0:
            length = max(0.1, (dx**2 + dy**2) ** 0.5)
            dx = (dx / length) * player_movement_speed
            dy = (dy / length) * player_movement_speed

        # Новая позиция в мировых координатах
        new_player_world_x = self.player_world_x + dx
        new_player_world_y = self.player_world_y + dy

        # Проверяем границы карты
        if 0 <= new_player_world_x <= self.map_width:
            self.player_world_x = new_player_world_x

        if 0 <= new_player_world_y <= self.map_height:
            self.player_world_y = new_player_world_y

        # Обновляем камеру (центрируем на игроке)
        player_offset_x, player_offset_y = self.update_camera()

        # Обновляем позицию игрока на экране
        # Если игрок у границы карты, он смещается от центра
        screen_center_x = WIDTH // 2
        screen_center_y = HEIGHT // 2

        if player_offset_x != 0:
            # Игрок у горизонтальной границы
            screen_x = screen_center_x + player_offset_x
        else:
            # Игрок в центре экрана
            screen_x = screen_center_x

        if player_offset_y != 0:
            # Игрок у вертикальной границы
            screen_y = screen_center_y + player_offset_y
        else:
            # Игрок в центре экрана
            screen_y = screen_center_y

        # Ограничиваем позицию игрока в пределах экрана
        screen_x = max(PLAYER_RADIUS, min(screen_x, WIDTH - PLAYER_RADIUS))
        screen_y = max(PLAYER_RADIUS, min(screen_y, HEIGHT - PLAYER_RADIUS))

        # Обновляем позицию игрока на экране
        self.player.x = screen_x
        self.player.y = screen_y

    def spawn_enemies(self, current_time):
        """Спавн врагов от границ видимой области"""
        if (
            current_time - self.last_enemy_spawn > self.enemy_spawn_delay
            and self.enemies_spawned < self.enemies_in_wave
            and len(self.enemies) < MAX_ENEMIES_ON_SCREEN
        ):
            # Получаем видимую область
            visible_area = self.get_visible_area()

            # Спавним врагов за пределами видимой области, но в пределах небольшого расстояния
            spawn_distance = 50  # Расстояние от границы экрана

            # Определяем с какой стороны спавнить врага
            side = random.choice(["top", "bottom", "left", "right"])

            if side == "top":
                enemy_world_x = random.randint(
                    visible_area.left - spawn_distance,
                    visible_area.right + spawn_distance,
                )
                enemy_world_y = (
                    visible_area.top - spawn_distance - ENEMY_MAX_RADIUS
                )

            elif side == "bottom":
                enemy_world_x = random.randint(
                    visible_area.left - spawn_distance,
                    visible_area.right + spawn_distance,
                )
                enemy_world_y = (
                    visible_area.bottom + spawn_distance + ENEMY_MAX_RADIUS
                )

            elif side == "left":
                enemy_world_x = (
                    visible_area.left - spawn_distance - ENEMY_MAX_RADIUS
                )
                enemy_world_y = random.randint(
                    visible_area.top - spawn_distance,
                    visible_area.bottom + spawn_distance,
                )

            else:  # right
                enemy_world_x = (
                    visible_area.right + spawn_distance + ENEMY_MAX_RADIUS
                )
                enemy_world_y = random.randint(
                    visible_area.top - spawn_distance,
                    visible_area.bottom + spawn_distance,
                )

            # Ограничиваем координаты в пределах карты
            enemy_world_x = max(
                ENEMY_MAX_RADIUS,
                min(enemy_world_x, self.map_width - ENEMY_MAX_RADIUS),
            )
            enemy_world_y = max(
                ENEMY_MAX_RADIUS,
                min(enemy_world_y, self.map_height - ENEMY_MAX_RADIUS),
            )

            # Преобразуем мировые координаты в экранные для создания врага
            screen_x, screen_y = self.world_to_screen(
                enemy_world_x, enemy_world_y
            )

            # Создаем врага
            enemy = Enemy(screen_x, screen_y)
            enemy.world_x = enemy_world_x
            enemy.world_y = enemy_world_y

            self.enemies.append(enemy)
            self.last_enemy_spawn = current_time
            self.enemies_spawned += 1

    def update_enemies(self):
        """Обновление позиций врагов"""
        for enemy in self.enemies[:]:
            # Враг двигается к мировым координатам игрока
            enemy.move_towards(self.player_world_x, self.player_world_y)

            # Обновляем экранные координаты врага
            enemy.x, enemy.y = self.world_to_screen(
                enemy.world_x, enemy.world_y
            )

            # Удаляем врагов, которые слишком далеко за пределами видимой области
            # visible_area = self.get_visible_area()
            # max_distance = 300  # Максимальное расстояние от видимой области
            #
            # if (
            #     enemy.world_x < visible_area.left - max_distance
            #     or enemy.world_x > visible_area.right + max_distance
            #     or enemy.world_y < visible_area.top - max_distance
            #     or enemy.world_y > visible_area.bottom + max_distance
            # ):
            #     self.enemies.remove(enemy)

    def update_experience(self):
        """Обновление позиций опыта"""
        for exp_orb in self.experience_orbs[:]:
            exp_orb.move_towards(self.player_world_x, self.player_world_y)

            exp_orb.x, exp_orb.y = self.world_to_screen(
                exp_orb.world_x, exp_orb.world_y
            )

            if exp_orb.check_collection(
                self.player.x, self.player.y, self.player.radius
            ):
                exp_gained = self.player.add_exp(exp_orb.value)
                self.total_exp_collected += exp_orb.value
                self.experience_orbs.remove(exp_orb)

                if exp_gained:
                    self.show_upgrade_screen()

    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        # Сброс позиции игрока и камеры
        self.player_world_x = self.map_width // 2
        self.player_world_y = self.map_height // 2
        self.camera_x = self.map_width // 2 - WIDTH // 2
        self.camera_y = self.map_height // 2 - HEIGHT // 2

        # Инициализация игрока
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.enemies = []
        self.experience_orbs = []
        self.damage_texts = []

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
                # exp_gained = self.player.add_exp(WAVE_REWARD_EXP)
                # self.total_exp_collected += WAVE_REWARD_EXP
                # if exp_gained:
                #     self.show_upgrade_screen()
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

    def check_collisions(self, current_time):
        """Проверка всех столкновений"""
        # Проверка столкновений врагов с игроком
        for enemy in self.enemies[:]:
            # Обновляем экранные координаты врага
            enemy.x, enemy.y = self.world_to_screen(
                enemy.world_x, enemy.world_y
            )

            if enemy.check_collision_with_player(
                self.player.x, self.player.y, self.player.radius
            ):
                if current_time - enemy.last_damage_deal > 500:
                    self.player.take_damage(enemy.damage)
                    enemy.last_damage_deal = current_time
                    if not self.player.is_alive:
                        self.game_over = True

        # Проверка столкновений снарядов с врагами
        for projectile in self.player.projectiles[:]:
            for enemy in self.enemies[:]:
                # Обновляем экранные координаты врага
                enemy.x, enemy.y = self.world_to_screen(
                    enemy.world_x, enemy.world_y
                )

                if projectile.check_collision(enemy.x, enemy.y, enemy.radius):
                    damage_dealt = projectile.damage
                    alive, actual_damage = enemy.take_damage(damage_dealt)

                    self.damage_texts.append(
                        DamageText(
                            enemy.x,
                            enemy.y - enemy.radius - 10,
                            damage_dealt,
                        )
                    )

                    if not alive:
                        # Создаем опыт на месте врага
                        self.experience_orbs.append(
                            Experience(
                                enemy.world_x, enemy.world_y, enemy.exp_value
                            )
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
        # Отрисовка карты с учетом смещения камеры
        self.screen.blit(self.map_image, (-self.camera_x, -self.camera_y))

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

        # Отрисовка экрана выбора улучшений
        if self.choosing_upgrade and self.upgrade_screen:
            self.upgrade_screen.draw(self.screen)

        # Отрисовка паузы
        elif self.paused and not self.choosing_upgrade:
            self.draw_pause_screen()

        # Отрисовка экрана окончания игры
        if self.game_over:
            draw_game_over(self.screen, player_stats, wave_info)

        # Отладочная информация
        self.draw_debug_info()

        pygame.display.flip()

    def draw_debug_info(self):
        """Отрисовка отладочной информации"""
        font = pygame.font.Font(None, 24)

        # info = [
        #     f"Глобальные координаты: ({int(self.player_world_x)}, {int(self.player_world_y)})",
        #     f"Камера: ({int(self.camera_x)}, {int(self.camera_y)})",
        #     f"Экранные координаты: ({int(self.player.x)}, {int(self.player.y)})",
        #     f"Волна: {self.wave}, Врагов: {len(self.enemies)}",
        # ]

        stats = self.player.get_stats()
        upgrades = [f"{k}: {v}" for k, v in stats.pop("upgrades").items()]
        info = [f"{k}: {v}" for k, v in stats.items()]
        info.extend(upgrades)

        for i, text in enumerate(info):
            text_surface = font.render(text, True, (255, 255, 0))
            self.screen.blit(text_surface, (255, 10 + i * 25))

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
                self.draw()
                self.clock.tick(FPS)
                continue

            # Управление игроком
            keys = pygame.key.get_pressed()
            self.move_player(keys)
            self.player.shoot(current_time)

            # Обновление снарядов
            self.player.update_projectiles()

            # Спавн врагов
            self.spawn_enemies(current_time)

            # Обновление волны
            self.update_wave()

            # Движение врагов
            self.update_enemies()

            # Движение опыта
            self.update_experience()

            # Проверка столкновений
            self.check_collisions(current_time)

            # Обновление текста урона
            for damage_text in self.damage_texts[:]:
                if not damage_text.update():
                    self.damage_texts.remove(damage_text)

            self.update_level_up_message(current_time)

            self.draw()

            self.clock.tick(FPS)
