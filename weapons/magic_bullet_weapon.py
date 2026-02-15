import pygame

from settings import (
    MAGIC_BULLET_MULTIPLIER_BULLETS,
    MAGIC_BULLET_MULTIPLIER_COOLDOWN,
    MAGIC_BULLET_MULTIPLIER_DAMAGE,
)
from weapons.types.projectile import Projectile
from weapons.weapon import Weapon


class MagicBulletWeapon(Weapon):
    """Оружие - магические пули, летящие к ближайшим врагам"""

    def __init__(self):
        super().__init__(
            name="magic_bullet",
            name_ui="Магическая пуля",
            damage=3,
            cooldown=1000,
            weapon_type="projectile",
        )
        self.projectiles = []
        self.max_projectiles = 3
        self.bullet_speed = 6

    def update(self, game):
        """Обновление пуль и проверка столкновений"""
        for bullet in self.projectiles[:]:
            bullet.update()

            if not bullet.active:
                self.projectiles.remove(bullet)
                continue

            # Если пуля столкнулась с врагом
            if bullet.is_collision():
                # Наносим урон врагу
                # bullet.target.take_damage(bullet.damage, game)
                # self.hit_enemies.append(bullet.target)
                # self.len_hit_enemies += 1
                self.add_enemy_to_hit(enemy=bullet.target)
                bullet.active = False

    def shoot(self, active_enemies):
        """Выстрел пулями к ближайшим врагам"""
        if not active_enemies:
            return

        # Сколько пуль можем выпустить
        bullets_to_shoot = self.max_projectiles - len(self.projectiles)

        if bullets_to_shoot <= 0:
            return

        # Берем ближайших врагов (максимум столько, сколько пуль можем выпустить)
        enemies_by_distance = sorted(
            active_enemies, key=lambda e: self.owner.distance_to(e)
        )[:bullets_to_shoot]

        # Создаем пули
        for enemy in enemies_by_distance:
            # Урон
            total_damage = self.damage + self.owner.get_damage()

            # Создаем пулю
            bullet = Projectile(
                self.owner.rect.centerx,
                self.owner.rect.centery,
                enemy,
                total_damage,
            )
            bullet.speed = self.bullet_speed

            self.projectiles.append(bullet)

        # Сбрасываем таймер атаки
        self.action_after_deal_damage()

    def draw(self, screen):
        """Отрисовка пуль"""
        for bullet in self.projectiles:
            bullet.draw(screen)

    def level_up(self):
        """Улучшение оружия"""
        self.level += 1
        # if self.level % 3 == 0:
        #     self.max_projectiles += MAGIC_BULLET_MULTIPLIER_BULLETS
        self.max_projectiles += MAGIC_BULLET_MULTIPLIER_BULLETS
        self.damage += MAGIC_BULLET_MULTIPLIER_DAMAGE
        self.cooldown -= MAGIC_BULLET_MULTIPLIER_COOLDOWN
        return True
