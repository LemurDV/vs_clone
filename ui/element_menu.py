import pygame

from settings import GREEN, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, YELLOW


class ElementMenu:
    """Меню выбора улучшений при повышении уровня"""

    def __init__(self, game):
        self.game = game
        self.active = False
        self.element_options = []
        self.selected_option = 0
        self.hovered_option = -1
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.last_key_time = 0
        self.key_delay = 200  # Задержка между нажатиями в мс

    def show(self, elements):
        """Показать меню с указанными улучшениями"""
        self.active = True
        self.element_options = elements[:3]  # Берем первые 3 улучшения
        self.selected_option = 0
        self.hovered_option = -1
        self.last_key_time = pygame.time.get_ticks()

    def hide(self):
        """Скрыть меню"""
        self.active = False
        self.element_options = []
        self.selected_option = 0
        self.hovered_option = -1

    def handle_keydown(self, key):
        """Обработка нажатия клавиши"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_key_time < self.key_delay:
            return

        self.last_key_time = current_time

        # Навигация
        if key == pygame.K_UP:
            self.selected_option = max(0, self.selected_option - 1)
        elif key == pygame.K_DOWN:
            self.selected_option = min(
                len(self.element_options) - 1, self.selected_option + 1
            )

        # Выбор с помощью клавиш 1-3 или Enter
        if key == pygame.K_RETURN:
            self.select_option(self.selected_option)
        elif key == pygame.K_1 and len(self.element_options) > 0:
            self.select_option(0)
        elif key == pygame.K_2 and len(self.element_options) > 1:
            self.select_option(1)
        elif key == pygame.K_3 and len(self.element_options) > 2:
            self.select_option(2)

    def handle_mouse_click(self, mouse_pos, button):
        """Обработка клика мыши"""
        if button == 1:  # Левая кнопка мыши
            for i in range(len(self.element_options)):
                option_rect = self.get_option_rect(i)
                if option_rect.collidepoint(mouse_pos):
                    self.select_option(i)
                    break

    def handle_mouse_motion(self, mouse_pos):
        """Обработка движения мыши"""
        for i in range(len(self.element_options)):
            option_rect = self.get_option_rect(i)
            if option_rect.collidepoint(mouse_pos):
                self.hovered_option = i
                self.selected_option = i  # Синхронизируем выбор с наведением
                break
        else:
            self.hovered_option = -1

    def get_option_rect(self, index):
        """Получить прямоугольник опции по индексу"""
        y_pos = 200 + index * 80
        return pygame.Rect(SCREEN_WIDTH // 2 - 200, y_pos, 400, 70)

    def select_option(self, index):
        """Выбрать опцию улучшения"""
        if 0 <= index < len(self.element_options):
            element = self.element_options[index]
            # element.apply(self.game.player)
            self.game.player.add_element(element)
            self.hide()
            # Уведомляем игру о выборе улучшения
            self.game.on_upgrade_selected()
            return True
        return False

    def draw(self, screen):
        """Отрисовка меню"""
        if not self.active or not self.element_options:
            return

        # Полупрозрачный фон
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # Заголовок
        title = self.font.render("ВЫБЕРИТЕ ЭЛЕМЕНТ", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Отображение опций улучшений
        for i, element in enumerate(self.element_options):
            y_pos = 200 + i * 80
            is_selected = i == self.selected_option
            is_hovered = i == self.hovered_option

            # Цвет рамки
            if is_selected or is_hovered:
                color = YELLOW
                border_width = 4
            else:
                color = WHITE
                border_width = 2

            # Рамка
            option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, y_pos, 400, 70)
            pygame.draw.rect(screen, color, option_rect, border_width)

            # Полупрозрачный фон для опции при наведении
            if is_hovered:
                hover_bg = pygame.Surface(
                    (option_rect.width - 4, option_rect.height - 4),
                    pygame.SRCALPHA,
                )
                hover_bg.fill((255, 255, 255, 30))
                screen.blit(hover_bg, (option_rect.x + 2, option_rect.y + 2))

            img_x = SCREEN_WIDTH // 2 - 190
            img_y = (
                y_pos + 19
            )  # Центрируем по вертикали в рамке (70/2 - 32/2 = 19)
            screen.blit(element.image, (img_x, img_y))

            # Текст улучшения (смещаем правее, чтобы освободить место для изображения)
            name_text = self.font.render(f"{element.name}", True, color)
            desc_text = self.small_font.render(
                f"{element.description}", True, WHITE
            )
            hotkey_text = self.small_font.render(f"[{i + 1}]", True, GREEN)

            text_offset = 40
            screen.blit(
                name_text, (SCREEN_WIDTH // 2 - 180 + text_offset, y_pos + 10)
            )
            screen.blit(
                desc_text, (SCREEN_WIDTH // 2 - 180 + text_offset, y_pos + 40)
            )
            screen.blit(hotkey_text, (SCREEN_WIDTH // 2 - 220, y_pos + 25))

        instr_lines = [
            "Используйте ↑↓ для навигации, Enter или 1-3 для выбора",
            "Или кликните мышью по нужному улучшению",
        ]

        for j, line in enumerate(instr_lines):
            instr_text = self.small_font.render(line, True, WHITE)
            screen.blit(
                instr_text,
                (
                    SCREEN_WIDTH // 2 - instr_text.get_width() // 2,
                    SCREEN_HEIGHT - 80 + j * 30,
                ),
            )
