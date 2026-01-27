import pygame

from settings import RED, WHITE, YELLOW


class DamageText:
    def __init__(self, x, y, damage, color=RED, is_critical=False):
        self.x = x
        self.y = y
        self.text = str(damage)
        self.base_color = color
        self.lifetime = 800
        self.creation_time = pygame.time.get_ticks()
        self.speed = 1.0
        self.font = pygame.font.Font(None, 28 if not is_critical else 36)
        self.active = True
        self.is_critical = is_critical

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.creation_time

        if elapsed > self.lifetime:
            self.active = False
            return

        # Всплытие вверх
        self.y -= self.speed

        # Плавное затухание
        progress = elapsed / self.lifetime
        self.alpha = int(255 * (1 - progress))

    def draw(self, screen):
        if not self.active:
            return

        text_surface = self.font.render(self.text, True, WHITE)

        final_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)

        # Выбираем цвет
        if self.is_critical:
            color = (*YELLOW, self.alpha)
        else:
            color = (*self.base_color, self.alpha)

        mask = pygame.mask.from_surface(text_surface)
        mask_surface = mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))

        final_surface.blit(mask_surface, (0, 0))

        # Рисуем
        screen.blit(
            final_surface,
            (
                self.x - final_surface.get_width() // 2,
                self.y - final_surface.get_height() // 2,
            ),
        )
