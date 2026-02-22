import math

from loguru import logger
import pygame

from weapons.weapon import Weapon, WeaponTypes


class LaserBeamWeapon(Weapon):
    def __init__(self):
        super().__init__(
            name="laser_beam",
            name_ui="Лазерный луч",
            damage=3,
            cooldown=2200,
            weapon_type=WeaponTypes.BEAM,
        )

        self.beam_length = 150
        self.beam_width = 6
        self.beam_duration = 3000
        self.beam_start_time = 0
        self.is_firing = False

        self.current_angle = 0

        self.beam_count = 1

        self.beam_color = (255, 50, 50)
        self.beam_opacity = 255

        self.active_beams = []

        self.last_damage_time = {}
        self.damage_interval = 500  # Урон раз в 0.5 секунды

    def update(self, game):
        current_time = pygame.time.get_ticks()

        if self.is_firing:
            elapsed = current_time - self.beam_start_time

            if elapsed < self.beam_duration:
                self.current_angle = (
                    (elapsed / self.beam_duration) * 2 * math.pi
                )

                # Плавное появление и исчезание
                progress = elapsed / self.beam_duration
                if progress < 0.2:  # Появление
                    self.beam_opacity = int(255 * (progress / 0.2))
                elif progress > 0.8:  # Исчезание
                    self.beam_opacity = int(255 * (1 - (progress - 0.8) / 0.2))
                else:
                    self.beam_opacity = 255

                # Обновляем позиции лучей
                self._update_beam_positions(game)

                # Проверяем попадания и наносим урон
                self._check_collisions_and_damage(game, current_time)
            else:
                # Луч исчез
                self.is_firing = False
                self.active_beams.clear()
                self.last_damage_time.clear()
                self.beam_opacity = 255

    def shoot(self, game):
        if self.is_firing:
            return

        player_center = self.owner.rect.center
        self.active_beams.clear()
        self.last_damage_time.clear()

        self._create_beams(player_center)

        self.is_firing = True
        self.beam_start_time = pygame.time.get_ticks()
        self.current_angle = 0
        self.beam_opacity = 255

        self._update_beam_positions(game)

        beam_word = "лучей" if self.beam_count > 1 else "луч"
        logger.debug(f"Лазер активирован: {self.beam_count} {beam_word}")

    def _create_beams(self, player_center):
        self.active_beams.clear()

        for i in range(self.beam_count):
            # Равномерно распределяем лучи по кругу
            angle_offset = (i / self.beam_count) * 2 * math.pi

            self.active_beams.append(
                {
                    "start": player_center,
                    "end": player_center,
                    "angle_offset": angle_offset,
                    "length": self.beam_length,
                    "width": self.beam_width,
                    "color": self.beam_color,
                }
            )

    def _update_beam_positions(self, game):
        player_center = self.owner.rect.center

        for beam in self.active_beams:
            # Вычисляем полный угол для этого луча
            total_angle = self.current_angle + beam["angle_offset"]

            # Вычисляем конечную точку
            end_x = player_center[0] + math.cos(total_angle) * beam["length"]
            end_y = player_center[1] + math.sin(total_angle) * beam["length"]

            # Обновляем позиции
            beam["start"] = player_center
            beam["end"] = (end_x, end_y)
            beam["direction"] = total_angle

    def _check_collisions_and_damage(self, game, current_time):
        active_enemies = game.enemy_manager.active_enemies

        if not active_enemies:
            return

        enemies_in_beam_now = set()

        for beam in self.active_beams:
            enemies_hit = self._get_enemies_in_beam(
                active_enemies,
                beam["start"],
                beam["end"],
                beam["direction"],
                beam["width"],
            )

            enemies_in_beam_now.update(enemies_hit)

        for enemy in enemies_in_beam_now:
            enemy_id = id(enemy)
            last_damage = self.last_damage_time.get(enemy_id, 0)

            if current_time - last_damage >= self.damage_interval:
                self.add_enemy_to_hit(enemy)
                self.last_damage_time[enemy_id] = current_time

    def _get_enemies_in_beam(
        self, enemies, start_pos, end_pos, direction, beam_width
    ):
        enemies_hit = []

        # Проверяем, что луч имеет ненулевую длину
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        beam_length_sq = dx * dx + dy * dy

        if beam_length_sq < 1:
            return enemies_hit

        # Нормализуем направление
        inv_length = 1.0 / math.sqrt(beam_length_sq)
        nx = dx * inv_length
        ny = dy * inv_length
        beam_length = math.sqrt(beam_length_sq)

        for enemy in enemies:
            if not enemy.active:
                continue

            # Вектор от начала луча до врага
            ex = enemy.rect.centerx - start_pos[0]
            ey = enemy.rect.centery - start_pos[1]

            # Проекция на луч
            projection = ex * nx + ey * ny

            if projection < 0 or projection > beam_length:
                continue

            # Ближайшая точка на луче
            closest_x = start_pos[0] + nx * projection
            closest_y = start_pos[1] + ny * projection

            # Расстояние до луча
            dist_sq = (enemy.rect.centerx - closest_x) ** 2 + (
                enemy.rect.centery - closest_y
            ) ** 2
            enemy_radius = enemy.rect.width / 2

            if dist_sq <= (enemy_radius + beam_width) ** 2:
                enemies_hit.append(enemy)

        return enemies_hit

    def draw(self, screen):
        if not self.is_firing or not self.owner or not self.active_beams:
            return

        for beam in self.active_beams:
            if "end" in beam and beam["end"] != beam["start"]:
                self._draw_beam(
                    screen, beam["start"], beam["end"], beam["color"]
                )

    def _draw_beam(self, screen, start_pos, end_pos, color):
        beam_surface = pygame.Surface(
            (screen.get_width(), screen.get_height()), pygame.SRCALPHA
        )

        color_with_alpha = (
            color[0],
            color[1],
            color[2],
            self.beam_opacity,
        )

        pygame.draw.line(
            beam_surface, color_with_alpha, start_pos, end_pos, self.beam_width
        )

        pygame.draw.circle(
            beam_surface,
            color_with_alpha,
            (int(end_pos[0]), int(end_pos[1])),
            self.beam_width // 2,
        )

        screen.blit(beam_surface, (0, 0))

    def level_up(self):
        self.level += 1

        self.damage += 1
        self.cooldown = max(1800, self.cooldown - 30)
        self.beam_length += 10

        if self.level % 3 == 0:
            self.beam_width += 1

        if self.level == 5:
            self.beam_count += 1
        elif self.level == 10:
            self.beam_count += 1

        return True

    @property
    def is_weapon(self):
        return True
