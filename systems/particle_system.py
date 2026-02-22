import random

from entities.damage_text import DamageText
from entities.heal_text import HealText
from settings import RED


class ParticleSystem:
    """Система управления частицами и эффектами"""

    def __init__(self):
        self.damage_texts = []
        self.particles = []
        self.heal_texts = []

        # Разный разброс для разных типов
        self.text_spread = 25
        self.heal_spread = 30
        self.critical_spread = 35

    def add_damage_text(self, x, y, damage, color=RED, is_critical=False):
        """Добавить текст урона со случайным смещением"""
        spread = self.critical_spread if is_critical else self.text_spread

        offset_x = random.randint(-spread, spread)
        offset_y = random.randint(-spread, spread)

        text = DamageText(
            x=x + offset_x,
            y=y + offset_y,
            damage=damage,
            color=color,
            is_critical=is_critical,
        )
        self.damage_texts.append(text)

    def add_particle(self, particle):
        """Добавить частицу"""
        self.particles.append(particle)

    def add_heal_text(self, x, y, heal):
        """Добавить текст хила со случайным смещением"""
        offset_x = random.randint(-self.text_spread, self.text_spread)
        offset_y = (
            random.randint(-self.text_spread, self.text_spread) - 10
        )  # Чуть выше

        text = HealText(x=x + offset_x, y=y + offset_y, heal=heal)
        self.heal_texts.append(text)

    def update(self):
        """Обновить все эффекты"""
        # Обновляем тексты урона
        for text in self.damage_texts[:]:
            text.update()
            if not text.active:
                self.damage_texts.remove(text)

        for heal_text in self.heal_texts[:]:
            heal_text.update()
            if not heal_text.active:
                self.heal_texts.remove(heal_text)

        # Обновляем частицы
        for particle in self.particles[:]:
            particle.update()
            if not particle.active:
                self.particles.remove(particle)

    def draw(self, screen):
        """Отрисовать все эффекты"""
        for particle in self.particles:
            particle.draw(screen)

        for text in self.damage_texts:
            text.draw(screen)

        for heal_text in self.heal_texts:
            heal_text.draw(screen)
