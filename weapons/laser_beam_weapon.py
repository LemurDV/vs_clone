import math
import pygame
import random

from loguru import logger
from weapons.weapon import Weapon
from settings import WHITE, RED, YELLOW, GREEN, BLUE


class LaserBeamWeapon(Weapon):
    """
    Оружие типа "луч" - моментальная атака по линии
    Луч появляется мгновенно и наносит урон всем врагам на своей длине
    """

    def __init__(self):
        super().__init__(
            name="laser_beam",
            name_ui="Лазерный луч",
            damage=10,
            cooldown=800,  # Быстрее чем коса, медленнее чем пули
            weapon_type="beam"
        )

        # Параметры луча
        self.beam_length = 300  # Длина луча
        self.beam_width = 4  # Толщина луча (базовая)
        self.beam_duration = 200  # Длительность отрисовки в мс
        self.beam_start_time = 0
        self.is_firing = False

        # Визуальные эффекты
        self.beam_opacity = 255
        self.beam_color = (255, 50, 50)  # Красный
        self.beam_particles = []  # Для частиц вдоль луча

        # Направление луча (в радианах)
        self.beam_direction = 0

        # Конечная точка луча (для отрисовки)
        self.beam_end_x = 0
        self.beam_end_y = 0

        # Список врагов, пораженных текущим лучом
        self.hit_enemies_current_beam = []

        # Уникальные эффекты
        self.penetration = True  # Луч проходит сквозь врагов
        self.knockback = 0  # Сила отбрасывания (будет расти с уровнем)
        self.burn_damage = 0  # Урон горением (будет расти с уровнем)
        self.burn_duration = 0  # Длительность горения в мс

        # Эффекты улучшений
        self.reflection_count = 0  # Количество отражений (для улучшения)
        self.beam_split = False  # Разделение луча (для улучшения)

    def update(self, game):
        """Обновление состояния луча"""
        current_time = pygame.time.get_ticks()

        # Обновляем активный луч
        if self.is_firing:
            # Вычисляем прозрачность для затухания
            elapsed = current_time - self.beam_start_time
            if elapsed < self.beam_duration:
                # Плавное затухание к концу
                self.beam_opacity = int(
                    255 * (1 - elapsed / self.beam_duration))

                # Обновляем частицы
                self._update_beam_particles(game)
            else:
                # Луч погас
                self.is_firing = False
                self.beam_particles.clear()
                self.hit_enemies_current_beam.clear()

    def shoot(self, game):
        """
        Выстрел лучом в направлении курсора или ближайшего врага
        """
        if self.is_firing:
            return

        # Определяем направление луча
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_center = self.owner.rect.center

        # Вычисляем направление от игрока к курсору
        dx = mouse_x - player_center[0]
        dy = mouse_y - player_center[1]

        if dx == 0 and dy == 0:
            dx, dy = 1, 0  # Направление по умолчанию

        self.beam_direction = math.atan2(dy, dx)

        # Вычисляем конечную точку луча
        self.beam_end_x = player_center[0] + math.cos(
            self.beam_direction) * self.beam_length
        self.beam_end_y = player_center[1] + math.sin(
            self.beam_direction) * self.beam_length

        # Активируем луч
        self.is_firing = True
        self.beam_start_time = pygame.time.get_ticks()
        self.beam_opacity = 255

        # Находим всех врагов на линии луча
        self._detect_enemies_in_beam(game.enemy_manager.active_enemies)

        # Создаем частицы для визуального эффекта
        self._create_beam_particles(game)

        # Если есть отражения, обрабатываем их
        if self.reflection_count > 0:
            self._handle_reflections(game)

    def _detect_enemies_in_beam(self, enemies):
        """
        Определяет врагов, находящихся на линии луча
        Используется алгоритм пересечения луча с прямоугольником врага
        """
        player_pos = pygame.math.Vector2(self.owner.rect.center)
        beam_end = pygame.math.Vector2(self.beam_end_x, self.beam_end_y)
        beam_direction_vec = (beam_end - player_pos).normalize()

        self.hit_enemies_current_beam.clear()

        for enemy in enemies:
            if not enemy.active:
                continue

            # Получаем центр врага
            enemy_pos = pygame.math.Vector2(enemy.rect.center)

            # Вектор от игрока к врагу
            to_enemy = enemy_pos - player_pos

            # Проекция вектора to_enemy на направление луча
            projection_length = to_enemy.dot(beam_direction_vec)

            # Проверяем, находится ли проекция в пределах длины луча
            if projection_length < 0 or projection_length > self.beam_length:
                continue

            # Точка на луче, ближайшая к врагу
            closest_point = player_pos + beam_direction_vec * projection_length

            # Расстояние от врага до линии луча
            distance_to_beam = enemy_pos.distance_to(closest_point)

            # Учитываем размер врага (радиус примерно половина ширины rect)
            enemy_radius = enemy.rect.width / 2

            # Если враг достаточно близко к линии луча
            if distance_to_beam <= enemy_radius + self.beam_width:
                self.add_enemy_to_hit(enemy)
                self.hit_enemies_current_beam.append(enemy)

                # Добавляем эффект горения, если есть
                if self.burn_damage > 0 and self.burn_duration > 0:
                    self._apply_burn_effect(enemy)

                # Добавляем отбрасывание, если есть
                if self.knockback > 0:
                    self._apply_knockback(enemy, beam_direction_vec)

    def _apply_burn_effect(self, enemy):
        """Применяет эффект горения к врагу"""
        # Здесь можно добавить систему статусов
        # Например, сохранять в словарь эффектов врага
        enemy.burn_damage = self.burn_damage
        enemy.burn_end_time = pygame.time.get_ticks() + self.burn_duration
        enemy.is_burning = True

    def _apply_knockback(self, enemy, direction):
        """Применяет отбрасывание к врагу"""
        enemy.knockback_vector = direction * self.knockback
        enemy.knockback_end_time = pygame.time.get_ticks() + 150  # 150 мс отбрасывания
        enemy.is_knocked_back = True

    def _handle_reflections(self, game):
        """
        Обрабатывает отражения луча от стен или врагов
        Для простоты - добавляем дополнительные лучи под углами
        """
        if self.reflection_count <= 0:
            return

        player_pos = self.owner.rect.center

        # Создаем дополнительные лучи под углами
        base_angle = self.beam_direction
        reflection_angles = []

        for i in range(self.reflection_count):
            # Добавляем лучи с отклонением 30 и -30 градусов
            angle_offset = math.radians(30 * (i + 1))
            reflection_angles.append(base_angle + angle_offset)
            reflection_angles.append(base_angle - angle_offset)

        # Временно сохраняем текущие параметры
        original_length = self.beam_length
        original_width = self.beam_width

        # Уменьшаем параметры для отражений
        self.beam_length = int(original_length * 0.7)
        self.beam_width = max(2, int(original_width * 0.6))

        # Создаем отраженные лучи
        for angle in reflection_angles:
            end_x = player_pos[0] + math.cos(angle) * self.beam_length
            end_y = player_pos[1] + math.sin(angle) * self.beam_length

            # Сохраняем текущие координаты
            original_end = (self.beam_end_x, self.beam_end_y)
            self.beam_end_x, self.beam_end_y = end_x, end_y

            # Определяем врагов для отраженного луча
            self._detect_enemies_in_beam(game.enemy_manager.active_enemies)

            # Восстанавливаем оригинальные координаты
            self.beam_end_x, self.beam_end_y = original_end

        # Восстанавливаем параметры
        self.beam_length = original_length
        self.beam_width = original_width

    def _create_beam_particles(self, game):
        """Создает частицы вдоль луча для визуального эффекта"""
        player_pos = pygame.math.Vector2(self.owner.rect.center)
        beam_end = pygame.math.Vector2(self.beam_end_x, self.beam_end_y)

        # Создаем частицы вдоль луча
        num_particles = 10
        for i in range(num_particles):
            t = i / (num_particles - 1)
            particle_pos = player_pos.lerp(beam_end, t)

            # Добавляем случайное смещение для реалистичности
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)

            # game.particle_system.add_effect(
            #     "laser_spark",
            #     particle_pos.x + offset_x,
            #     particle_pos.y + offset_y,
            #     color=self.beam_color,
            #     size=random.randint(2, 4)
            # )

    def _update_beam_particles(self, game):
        """Обновляет существующие частицы"""
        # Можно добавить пульсацию или свечение
        pass

    def draw(self, screen):
        """Отрисовка луча"""
        if not self.is_firing or not self.owner:
            return

        player_center = self.owner.rect.center

        # Рисуем основной луч
        self._draw_beam(screen, player_center,
                        (self.beam_end_x, self.beam_end_y),
                        self.beam_color, self.beam_opacity)

        # Рисуем свечение вокруг луча (эффект)
        if self.beam_opacity > 100:
            glow_color = (255, 255, 255, self.beam_opacity // 3)
            self._draw_beam(screen, player_center,
                            (self.beam_end_x, self.beam_end_y),
                            glow_color, self.beam_opacity // 3,
                            width=self.beam_width + 4)

        # Рисуем информацию о луче (для дебага)
        self._draw_beam_info(screen, player_center)

    def _draw_beam(self, screen, start_pos, end_pos, color, opacity,
                   width=None):
        """Рисует луч с заданными параметрами"""
        if width is None:
            width = self.beam_width

        # Создаем поверхность с прозрачностью
        beam_surface = pygame.Surface((screen.get_width(), screen.get_height()),
                                      pygame.SRCALPHA)

        # Рисуем линию
        pygame.draw.line(
            beam_surface,
            (*color[:3], opacity),  # Добавляем альфа-канал
            start_pos,
            end_pos,
            width
        )

        # Добавляем круг на конце луча
        end_glow_radius = width * 2
        pygame.draw.circle(
            beam_surface,
            (*color[:3], opacity // 2),
            (int(end_pos[0]), int(end_pos[1])),
            end_glow_radius
        )

        # Добавляем круг в начале (у игрока)
        pygame.draw.circle(
            beam_surface,
            (*color[:3], opacity),
            (int(start_pos[0]), int(start_pos[1])),
            width
        )

        screen.blit(beam_surface, (0, 0))

    def _draw_beam_info(self, screen, player_center):
        """Рисует информацию о луче (для отладки)"""
        # Создаем текст с параметрами
        font = pygame.font.Font(None, 20)

        # Информация о длине и ширине
        info_text = f"Length: {self.beam_length}  Width: {self.beam_width}"
        if self.burn_damage > 0:
            info_text += f"  Burn: {self.burn_damage}"
        if self.reflection_count > 0:
            info_text += f"  Reflect: {self.reflection_count}"

        text = font.render(info_text, True, WHITE)
        screen.blit(text, (player_center[0] - 100, player_center[1] - 50))

        # Информация о количестве пораженных врагов
        hit_text = font.render(
            f"Hit: {len(self.hit_enemies_current_beam)} enemies",
            True,
            GREEN if self.hit_enemies_current_beam else RED
        )
        screen.blit(hit_text, (player_center[0] - 100, player_center[1] - 30))

    def level_up(self):
        """Улучшение лазерного луча"""
        self.level += 1

        # Базовые улучшения
        self.damage += 5
        self.cooldown = max(400, self.cooldown - 50)  # Уменьшаем кулдаун

        # Улучшения в зависимости от уровня
        if self.level == 2:
            # Увеличиваем длину и ширину
            self.beam_length += 50
            self.beam_width += 2
            self.name_ui = "Усиленный лазер"

        elif self.level == 3:
            # Добавляем эффект горения
            self.burn_damage = 2
            self.burn_duration = 3000  # 3 секунды
            self.name_ui = "Жгучий лазер"

        elif self.level == 4:
            # Увеличиваем длину и добавляем отражения
            self.beam_length += 75
            self.reflection_count = 1  # Добавляем 1 отражение
            self.beam_width += 2
            self.name_ui = "Отражающий лазер"

        elif self.level == 5:
            # Максимальный уровень - добавляем расщепление и отбрасывание
            self.beam_split = True
            self.reflection_count = 2
            self.knockback = 50
            self.beam_length += 100
            self.damage += 10
            self.name_ui = "Разящий лазер"

        # Каждые 2 уровня увеличиваем длину
        if self.level % 2 == 0:
            self.beam_length += 25

        logger.info(f"Луч улучшен до {self.level} уровня: {self.name_ui}")
        return True

    @property
    def is_weapon(self):
        return True