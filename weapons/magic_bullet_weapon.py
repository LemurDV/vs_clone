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
            self.shoot(game.enemy_manager.enemies)

    def shoot(self, enemies):
        """Выстрел пулями"""
        # Ищем активных врагов
        active_enemies = [e for e in enemies if e.active]

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
        self.level += 1
        if self.level % 3 == 0:
            self.max_bullets += 1
        self.damage += 2
        self.cooldown -= 30
        return True

    def increase_damage(self):
        self.damage += 2

    def decrease_cooldown(self):
        self.cooldown -= 30

    @property
    def is_weapon(self):
        """Является ли улучшением-оружием"""
        return True
