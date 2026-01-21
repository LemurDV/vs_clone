import random

import pygame


class DamageText:
    def __init__(self, x, y, damage, is_crit=False):
        self.x = x
        self.y = y - 20
        self.damage = str(int(damage))
        self.is_crit = is_crit
        self.lifetime = 1000
        self.created_time = pygame.time.get_ticks()
        self.velocity_y = -1.5
        self.velocity_x = random.uniform(-0.5, 0.5)  # Случайное смещение по X

    def update(self):
        current_time = pygame.time.get_ticks()
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.05
        return current_time - self.created_time < self.lifetime

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        age = current_time - self.created_time

        if self.is_crit:
            font_size = 28
            color = (255, 255, 0)  # Желтый для крита
        else:
            font_size = 22
            color = (255, 100, 100)  # Красный для обычного урона

        font = pygame.font.Font(None, font_size)
        text_surface = font.render(self.damage, True, color)

        # Устанавливаем прозрачность
        alpha = 255 * (1 - age / self.lifetime)
        text_surface.set_alpha(int(alpha))

        # Центрируем текст
        text_rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text_surface, text_rect)
