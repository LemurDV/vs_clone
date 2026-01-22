import pygame
from config import *


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.selected_level = None

        # Цвета для каждого уровня
        self.level_colors = {
            1: (50, 50, 100),  # Темно-синий
            2: (100, 50, 50),  # Темно-красный
            3: (50, 100, 50)  # Темно-зеленый
        }

        # Параметры кнопок
        self.button_width = 200
        self.button_height = 60
        self.button_margin = 20

        # Создаем кнопки для уровней
        self.level_buttons = []
        self.create_buttons()

    def create_buttons(self):
        """Создание кнопок для выбора уровней"""
        total_height = len(self.level_colors) * self.button_height + \
                       (len(self.level_colors) - 1) * self.button_margin

        start_y = (HEIGHT - total_height) // 2

        for level, color in self.level_colors.items():
            button_rect = pygame.Rect(
                WIDTH // 2 - self.button_width // 2,
                start_y,
                self.button_width,
                self.button_height
            )

            self.level_buttons.append({
                "rect": button_rect,
                "level": level,
                "color": color,
                "hovered": False,
                "text_color": (230, 230, 230)
            })

            start_y += self.button_height + self.button_margin

    def handle_events(self):
        """Обработка событий в меню"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False, None
                # Выбор уровня с помощью цифр 1-3
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    level = int(event.unicode)
                    if level in self.level_colors:
                        return False, level

            elif event.type == pygame.MOUSEMOTION:
                for button in self.level_buttons:
                    button["hovered"] = button["rect"].collidepoint(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    for button in self.level_buttons:
                        if button["rect"].collidepoint(event.pos):
                            return False, button["level"]

        return True, None

    def draw(self):
        """Отрисовка меню"""
        # Заливка фона цветом в зависимости от наведения на кнопку
        bg_color = BLACK

        # Если навели на кнопку, используем цвет уровня для фона
        for button in self.level_buttons:
            if button["hovered"]:
                # Создаем более светлую версию цвета уровня для фона
                bg_color = tuple(min(255, c + 30) for c in button["color"])
                break

        self.screen.fill(bg_color)

        # Заголовок
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("ВЫБЕРИТЕ УРОВЕНЬ", True, WHITE)
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Подзаголовок
        subtitle_font = pygame.font.Font(None, 28)
        subtitle_text = subtitle_font.render(
            "Наведите курсор на уровень для предпросмотра",
            True, (200, 200, 255)
        )
        self.screen.blit(subtitle_text,
                         (WIDTH // 2 - subtitle_text.get_width() // 2, 170))

        # Отрисовка кнопок уровней
        for button in self.level_buttons:
            self.draw_button(button)

        # Подсказка
        hint_font = pygame.font.Font(None, 24)
        hint_text = hint_font.render(
            "Нажмите ESC для выхода, или цифру 1-3 для выбора уровня",
            True, (180, 180, 180)
        )
        self.screen.blit(hint_text,
                         (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 50))

        pygame.display.flip()

    def draw_button(self, button):
        """Отрисовка отдельной кнопки"""
        rect = button["rect"]
        color = button["color"]
        hovered = button["hovered"]
        text_color = button["text_color"]

        # Если кнопка наведена, делаем ее светлее
        if hovered:
            button_color = tuple(min(255, c + 50) for c in color)
            border_color = WHITE
            border_width = 4
        else:
            button_color = color
            border_color = tuple(min(255, c + 100) for c in color)
            border_width = 2

        # Фон кнопки
        pygame.draw.rect(self.screen, button_color, rect, border_radius=12)
        pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=12)

        # Текст кнопки
        font = pygame.font.Font(None, 36)
        text = font.render(f"Уровень {button['level']}", True, text_color)

        self.screen.blit(text, (
            rect.x + rect.width // 2 - text.get_width() // 2,
            rect.y + rect.height // 2 - text.get_height() // 2
        ))

        # Иконка уровня
        icon_font = pygame.font.Font(None, 30)
        icon = "⭐" * button['level']  # Звезды по количеству уровня
        icon_text = icon_font.render(icon, True, text_color)

        self.screen.blit(icon_text, (
            rect.x + rect.width // 2 - icon_text.get_width() // 2,
            rect.y + rect.height // 2 + text.get_height() // 2 + 5
        ))

    def run(self):
        """Запуск меню"""
        while self.running:
            self.running, self.selected_level = self.handle_events()

            if not self.running or self.selected_level is not None:
                break

            self.draw()
            pygame.time.Clock().tick(FPS)

        return self.selected_level