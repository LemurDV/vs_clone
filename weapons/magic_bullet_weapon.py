from settings import *
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
        )
        self.bullets = []
        self.max_bullets = 1
        self.bullet_speed = 6
        self.upgrade_levels = [
            {"max_bullets": 2, "damage": 4, "cooldown": 800},
            {"max_bullets": 3, "damage": 5, "cooldown": 700},
            {"max_bullets": 4, "damage": 6, "cooldown": 600},
            {"max_bullets": 4, "damage": 6, "cooldown": 600},
        ]

    def update(self, game):
        """Обновление оружия"""
        # Обновление существующих пуль
        for bullet in self.bullets[:]:
            if bullet.active:
                bullet.update(game)
            else:
                self.bullets.remove(bullet)

        # Стрельба
        if self.can_attack() and self.owner and self.owner.active:
            self.shoot(game)

    def shoot(self, game):
        """Выстрел пулями"""
        # Ищем активных врагов
        active_enemies = [e for e in game.enemies if e.active]

        if not active_enemies:
            return

        # Определяем, сколько пуль можем выпустить
        bullets_to_shoot = min(
            self.max_bullets - len(self.bullets), len(active_enemies)
        )

        if bullets_to_shoot <= 0:
            return

        # Выбираем ближайших врагов
        enemies_by_distance = sorted(
            active_enemies, key=lambda e: self.owner.distance_to(e)
        )

        for i in range(bullets_to_shoot):
            if i < len(enemies_by_distance):
                target = enemies_by_distance[i]
                owner_damage = (
                    self.owner.get_damage()
                    if hasattr(self.owner, "get_damage")
                    else 1
                )
                total_damage = self.damage * owner_damage

                bullet = Projectile(
                    self.owner.rect.centerx,
                    self.owner.rect.centery,
                    target,
                    total_damage,
                )
                self.bullets.append(bullet)

        self.last_attack_time = pygame.time.get_ticks()

    def draw(self, screen):
        """Отрисовка пуль"""
        for bullet in self.bullets:
            bullet.draw(screen)

    def level_up(self):
        """Улучшение оружия"""
        if self.level < self.max_level:
            self.level += 1
            level_info = self.upgrade_levels[self.level - 1]
            self.max_bullets = level_info["max_bullets"]
            self.damage = level_info["damage"]
            self.cooldown = level_info["cooldown"]
            return True
        return False

    @property
    def is_weapon(self):
        """Является ли улучшением-оружием"""
        return True
