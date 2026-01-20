# upgrade_screen.py
import pygame

from config import *


class UpgradeScreen:
    def __init__(self, player):
        self.player = player
        self.available_upgrades = player.get_available_upgrades(
            UPGRADES_PER_LEVEL
        )
        self.selected_upgrade = None
        self.upgrade_buttons = []
        self.create_buttons()

    def create_buttons(self):
        """Создание кнопок для выбора улучшений"""
        total_width = (
            UPGRADES_PER_LEVEL * UPGRADE_BUTTON_WIDTH
            + (UPGRADES_PER_LEVEL - 1) * UPGRADE_BUTTON_MARGIN
        )
        start_x = (WIDTH - total_width) // 2
        y = HEIGHT // 2 - UPGRADE_BUTTON_HEIGHT // 2

        for i, upgrade_type in enumerate(self.available_upgrades):
            x = start_x + i * (UPGRADE_BUTTON_WIDTH + UPGRADE_BUTTON_MARGIN)
            self.upgrade_buttons.append(
                {
                    "rect": pygame.Rect(
                        x, y, UPGRADE_BUTTON_WIDTH, UPGRADE_BUTTON_HEIGHT
                    ),
                    "type": upgrade_type,
                    "hovered": False,
                }
            )

    def handle_event(self, event):
        """Обработка событий на экране улучшений"""
        if event.type == pygame.MOUSEMOTION:
            for button in self.upgrade_buttons:
                button["hovered"] = button["rect"].collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                for button in self.upgrade_buttons:
                    if button["rect"].collidepoint(event.pos):
                        self.selected_upgrade = button["type"]
                        return True

        elif event.type == pygame.KEYDOWN:
            # Выбор улучшения с помощью цифр 1-3
            if event.key == pygame.K_1 and len(self.upgrade_buttons) > 0:
                self.selected_upgrade = self.upgrade_buttons[0]["type"]
                return True
            elif event.key == pygame.K_2 and len(self.upgrade_buttons) > 1:
                self.selected_upgrade = self.upgrade_buttons[1]["type"]
                return True
            elif event.key == pygame.K_3 and len(self.upgrade_buttons) > 2:
                self.selected_upgrade = self.upgrade_buttons[2]["type"]
                return True

        return False

    def draw(self, screen):
        """Отрисовка экрана выбора улучшений"""
        # Полупрозрачный фон
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 50))
        screen.blit(overlay, (0, 0))

        # Заголовок
        title_font = pygame.font.Font(None, 64)
        title_text = title_font.render(
            "ВЫБЕРИТЕ УЛУЧШЕНИЕ", True, (255, 255, 100)
        )
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Уровень игрока
        level_font = pygame.font.Font(None, 48)
        level_text = level_font.render(
            f"Уровень {self.player.level + 1}", True, WHITE
        )
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 180))

        # Отрисовка кнопок улучшений
        for i, button in enumerate(self.upgrade_buttons):
            self.draw_upgrade_button(screen, button, i + 1)

        # Подсказка
        hint_font = pygame.font.Font(None, 28)
        hint_text = hint_font.render(
            "Нажмите 1, 2 или 3 для выбора, или кликните мышью",
            True,
            (200, 200, 255),
        )
        screen.blit(
            hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 100)
        )

    def draw_upgrade_button(self, screen, button, number):
        """Отрисовка кнопки улучшения"""
        rect = button["rect"]
        upgrade_type = button["type"]
        hovered = button["hovered"]

        # Цвет фона кнопки
        if hovered:
            color = UPGRADES[upgrade_type]["color"]
            border_color = (255, 255, 255)
            border_width = 4
        else:
            # Немного темнее цвет
            color = tuple(
                max(0, c - 30) for c in UPGRADES[upgrade_type]["color"]
            )
            border_color = (150, 150, 150)
            border_width = 2

        # Фон кнопки
        pygame.draw.rect(screen, color, rect, border_radius=15)
        pygame.draw.rect(
            screen, border_color, rect, border_width, border_radius=15
        )

        # Номер кнопки
        number_font = pygame.font.Font(None, 36)
        number_text = number_font.render(f"{number}", True, WHITE)
        screen.blit(number_text, (rect.x + 15, rect.y + 15))

        # Название улучшения
        name_font = pygame.font.Font(None, 32)
        name = UPGRADES[upgrade_type]["name"]
        name_text = name_font.render(name, True, WHITE)
        screen.blit(
            name_text,
            (
                rect.x + rect.width // 2 - name_text.get_width() // 2,
                rect.y + 20,
            ),
        )

        # Иконка
        icon_font = pygame.font.Font(None, 48)
        icon_text = icon_font.render(
            UPGRADES[upgrade_type]["icon"], True, WHITE
        )
        screen.blit(
            icon_text,
            (
                rect.x + rect.width // 2 - icon_text.get_width() // 2,
                rect.y + 50,
            ),
        )

        # Описание
        desc_font = pygame.font.Font(None, 22)
        description = self.player.get_upgrade_description(upgrade_type)

        # Разбиваем описание на строки
        lines = description.split("\n")
        for j, line in enumerate(lines):
            desc_text = desc_font.render(line, True, (230, 230, 230))
            screen.blit(
                desc_text,
                (
                    rect.x + rect.width // 2 - desc_text.get_width() // 2,
                    rect.y + 90 + j * 25,
                ),
            )
