import random


class CollisionSystem:
    def __init__(self, game):
        self.game = game
        self.player = game.player

    def update(self):
        for weapon in self.game.player.weapons.values():
            if weapon.weapon_type == "aura" and weapon.can_attack():
                self.check_aura_weapon(weapon)
            elif weapon.weapon_type == "projectile":
                self.check_projectile_weapon(weapon)
            elif weapon.weapon_type == "melee":
                self.check_melee_weapon(weapon)

        magic_bullet = self.game.player.weapons.get("magic_bullet")
        if magic_bullet:
            self.check_bullets_collisions(magic_bullet)

    def check_aura_weapon(self, weapon):
        """Проверка ауры"""
        for enemy in self.game.enemy_manager.enemies[:]:
            if weapon.is_collision(enemy=enemy):
                damage = weapon.get_damage()
                self.deal_damage(enemy=enemy, damage=damage)
        self.actions_after_deal_damage(weapon=weapon)

    def check_projectile_weapon(self, weapon):
        """Проверка возможности выстрела новых пуль"""
        if weapon.can_attack():
            weapon.shoot(self.game.enemy_manager.enemies)
            self.actions_after_deal_damage(weapon=weapon)

    def check_melee_weapon(self, weapon):
        if weapon.can_attack():
            weapon.shoot(self.game.enemy_manager.enemies, self.game)
            self.actions_after_deal_damage(weapon=weapon)

    def actions_after_deal_damage(self, weapon):
        if self.player.vampire and weapon.hit_enemies > 0:
            total_vampire = weapon.hit_enemies * self.player.vampire
            self.player.heal(total_vampire)
            self.game.particle_system.add_heal_text(
                x=self.player.x,
                y=self.player.y,
                heal=total_vampire,
            )
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
