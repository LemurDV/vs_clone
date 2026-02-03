import random


class CollisionSystem:
    def __init__(self, game):
        self.game = game

    def update(self):
        for weapon in self.game.player.weapons.values():
            if weapon.name == "aura" and weapon.can_attack():
                self.check_aura_weapon(weapon)
            elif weapon.name == "magic_bullet":
                self.check_magic_bullet_weapon(weapon)
            elif weapon.name == "lightning_ball":
                self.check_magic_bullet_weapon(weapon)

        magic_bullet = self.game.player.weapons.get("magic_bullet")
        if magic_bullet:
            self.check_bullets_collisions(magic_bullet)

    def check_aura_weapon(self, weapon):
        """Проверка ауры"""
        for enemy in self.game.enemy_manager.enemies[:]:
            if weapon.is_collision(enemy=enemy):
                damage = weapon.get_damage()
                self.deal_damage(enemy=enemy, damage=damage)
        weapon.action_after_deal_damage()

    def check_magic_bullet_weapon(self, weapon):
        """Проверка возможности выстрела новых пуль"""
        if weapon.can_attack():
            weapon.shoot(self.game.enemy_manager.enemies)
            weapon.action_after_deal_damage()

    def check_bullets_collisions(self, weapon):
        """Проверка столкновений существующих пуль"""
        for bullet in weapon.bullets[:]:
            if not bullet.active:
                continue

            # Обновляем позицию пули
            bullet.update()

            # Проверяем столкновение с целью
            if bullet.target.active and bullet.is_collision():
                damage = bullet.damage
                self.deal_damage(enemy=bullet.target, damage=damage)
                bullet.active = False
                weapon.bullets.remove(bullet)

    def deal_damage(self, enemy, damage):
        is_critical = random.random() < 0.1
        if is_critical:
            damage *= 1.5

        if enemy.take_damage(int(damage), self.game, is_critical):
            self.game.enemy_died(enemy)
