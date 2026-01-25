# ui/hud.py
import pygame

from settings import *


class BaseHud:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(None, 24)

    def draw_ui(self):
        """Отрисовка интерфейса"""
        self.draw_player_stats()
        self.draw_enemy_stats()
        self.draw_time()
        self.draw_controls()
        self.draw_weapon_stats()
        self.draw_pause_indicator()

    def draw_player_stats(self):
        """Отрисовка статистики игрока"""
        # Здоровье
        self.heart_image = pygame.image.load(
            "assets/stats/heart.png"
        ).convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (20, 20))
        self.screen.blit(self.heart_image, (10, 10))
        health_text = self.font.render(
            f"{self.game.player.health}/{self.game.player.max_health}",
            True,
            WHITE,
        )
        self.screen.blit(health_text, (35, 10))

        exp_needed = self.game.player.experience_needed
        exp_text = self.font.render(
            f"Уровень: {self.game.player.level} | Опыт: {self.game.player.experience}/{exp_needed}",
            True,
            WHITE,
        )
        self.screen.blit(exp_text, (10, 40))

    def draw_enemy_stats(self):
        """Отрисовка статистики врагов"""
        enemies_len = len(self.game.enemy_manager.enemies)
        enemies_text = self.font.render(
            f"Врагов: {enemies_len} | Убито: {self.game.enemies_killed}",
            True,
            WHITE,
        )
        self.screen.blit(enemies_text, (10, 70))

    def draw_time(self):
        """Отрисовка времени игры"""
        minutes = self.game.game_time // 60000
        seconds = (self.game.game_time % 60000) // 1000
        time_text = self.font.render(
            f"Время: {minutes:02d}:{seconds:02d}", True, WHITE
        )
        self.screen.blit(time_text, (SCREEN_WIDTH - 150, 10))

    def draw_controls(self):
        """Отрисовка инструкций управления"""
        if not self.game.game_paused:
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

    def draw_weapon_stats(self):
        """Отрисовка статистики оружия"""
        y_pos = 100
        for weapon in self.game.player.weapons.values():
            weapon_text = self.font.render(
                f"{weapon.name} (Ур. {weapon.level})", True, WHITE
            )
            self.screen.blit(weapon_text, (10, y_pos))
            y_pos += 25

    def draw_pause_indicator(self):
        """Отрисовка индикатора паузы"""
        if self.game.game_paused:
            pause_text = self.font.render(
                "ПАУЗА: Выбор улучшения", True, YELLOW
            )
            self.screen.blit(
                pause_text,
                (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 20),
            )
