import math

import pygame

from weapons.weapon import Weapon


class OrbitingWeapon(Weapon):
    def __init__(
        self, name, damage, orbit_radius, speed, owner, color=(50, 200, 50)
    ):
        super().__init__(name, damage, 200, owner)
        self.orbit_radius = orbit_radius
        self.speed = speed
        self.angle = 0
        self.projectile_count = 1
        self.projectiles = []
        self.color = color

    def update(self, current_time, enemies):
        """Обновление позиций и проверка столкновений"""
        # Обновляем угол вращения
        self.angle += self.speed

        # Рассчитываем позиции снарядов
        self.projectiles = []
        for i in range(self.projectile_count):
            angle = self.angle + (i * 2 * math.pi / self.projectile_count)
            x = self.owner.x + math.cos(angle) * self.orbit_radius
            y = self.owner.y + math.sin(angle) * self.orbit_radius
            self.projectiles.append((x, y))

            # Проверяем столкновения с врагами только если прошел кулдаун
            if current_time - self.last_attack > self.cooldown:
                for enemy in enemies[:]:
                    dx = enemy.x - x
                    dy = enemy.y - y
                    distance = math.sqrt(dx * dx + dy * dy)

                    if distance < 10 + enemy.radius:  # 10 - радиус снаряда
                        alive, damage_dealt = enemy.take_damage(
                            self.damage * self.level
                        )
                        if not alive:
                            # Если враг умер, можно добавить эффект
                            pass
                        self.last_attack = current_time
                        break  # Один снаряд поражает только одного врага за атаку

    def draw(self, screen):
        """Рисуем орбитальные снаряды"""
        for x, y in self.projectiles:
            pygame.draw.circle(screen, self.color, (int(x), int(y)), 10)
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 10, 2)

    def level_up(self, player_dmg):
        """Улучшение - добавляем снаряды"""
        super().level_up()
        if self.level % 2 == 0:  # Каждые 2 уровня
            self.projectile_count += 1
        self.damage = int(self.damage * 1.3)  # +30% урона за уровень
