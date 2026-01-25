# entities/damage_text.py
import pygame
from settings import *


class DamageText:
    """Текст урона, всплывающий над врагами"""

    def __init__(self, x, y, damage, color=RED):
        self.x = x
        self.y = y
        self.text = str(damage)
        self.color = color
        self.lifetime = 800  # Время жизни в мс
        self.creation_time = pygame.time.get_ticks()
        self.speed = 1.0  # Скорость всплытия
        self.font = pygame.font.Font(None, 24)
        self.active = True

    def update(self):
        """Обновление текста урона"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.creation_time

        if elapsed > self.lifetime:
            self.active = False
            return

        # Всплытие вверх
        self.y -= self.speed

        # Прозрачность (затухание)
        alpha = 255 - int((elapsed / self.lifetime) * 255)
        self.color = (self.color[0], self.color[1], self.color[2], alpha)

    def draw(self, screen):
        """Отрисовка текста урона"""
        if not self.active:
            return

        # Создаем поверхность с альфа-каналом
        text_surface = self.font.render(self.text, True, self.color)

        # Применяем альфа-канал если нужно
        if len(self.color) == 4:
            alpha_surface = pygame.Surface(text_surface.get_size(),
                                           pygame.SRCALPHA)
            alpha_surface.blit(text_surface, (0, 0))
            alpha_surface.set_alpha(self.color[3])
            text_surface = alpha_surface

        screen.blit(text_surface,
                    (self.x - text_surface.get_width() // 2, self.y))