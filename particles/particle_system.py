import pygame
from settings import *
from entities.damage_text import DamageText


class ParticleSystem:
    """Система управления частицами и эффектами"""

    def __init__(self):
        self.damage_texts = []
        self.particles = []  # Для будущих эффектов (вспышки, искры и т.д.)

    def add_damage_text(self, x, y, damage, color=RED, is_critical=False):
        """Добавить текст урона"""
        text = DamageText(x, y, damage, color, is_critical)
        self.damage_texts.append(text)

    def add_particle(self, particle):
        """Добавить частицу"""
        self.particles.append(particle)

    def update(self):
        """Обновить все эффекты"""
        # Обновляем тексты урона
        for text in self.damage_texts[:]:
            text.update()
            if not text.active:
                self.damage_texts.remove(text)

        # Обновляем частицы
        for particle in self.particles[:]:
            particle.update()
            if not particle.active:
                self.particles.remove(particle)

    def draw(self, screen):
        """Отрисовать все эффекты"""
        # Рисуем частицы (под текстами)
        for particle in self.particles:
            particle.draw(screen)

        # Рисуем тексты урона (поверх частиц)
        for text in self.damage_texts:
            text.draw(screen)