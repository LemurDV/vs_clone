import random

from entities import Enemy
from weapons.lightning_ball_weapon import LightningBallWeapon
from weapons.magic_bullet_weapon import MagicBulletWeapon
from weapons.scythe import ScytheWeapon


class CollisionSystem:
    def __init__(self, game):
        self.game = game
        self.player = game.player

    def update(self):
        for weapon in self.game.player.weapons.values():
            if weapon.can_attack():
                if weapon.weapon_type == "aura":
                    self.aura_weapon_actions(weapon)
                elif weapon.weapon_type == "projectile":
                    self.projectile_weapon_actions(weapon)
                elif weapon.weapon_type == "melee":
                    self.melee_weapon_actions(weapon)

                if weapon.hit_enemies:
                    self.deal_damage_to_enemies(
                        enemies=weapon.hit_enemies,
                        weapon=weapon,
                    )
                    self.actions_after_deal_damage(weapon=weapon)

        projectile_weapon = self.game.player.weapons.get("projectile")
        if projectile_weapon:
            self.check_projectiles_collisions(projectile_weapon)

    def aura_weapon_actions(self, weapon):
        for enemy in self.game.enemy_manager.enemies[:]:
            if weapon.is_collision(enemy=enemy):
                weapon.add_enemy_to_hit(enemy=enemy)
                # damage = weapon.get_damage()
                # self.deal_damage(enemy=enemy, damage=damage)
        # self.actions_after_deal_damage(weapon=weapon)

    def projectile_weapon_actions(
        self, weapon: MagicBulletWeapon | LightningBallWeapon
    ):
        weapon.shoot(self.game.enemy_manager.enemies)
        # self.actions_after_deal_damage(weapon=weapon)

    def melee_weapon_actions(self, weapon: ScytheWeapon):
        active_enemies = self.game.enemy_manager.active_enemies
        weapon.shoot(active_enemies=active_enemies, game=self.game)
        weapon.detect_enemies_in_range(
            enemies=active_enemies,
            direction=weapon.attack_direction,
        )
        # self.actions_after_deal_damage(weapon=weapon)

    def actions_after_deal_damage(self, weapon):
        if self.player.vampire and weapon.len_hit_enemies > 0:
            total_vampire = weapon.len_hit_enemies * self.player.vampire
            self.player.heal(total_vampire)
            self.game.particle_system.add_heal_text(
                x=self.player.x,
                y=self.player.y,
                heal=total_vampire,
            )
        weapon.action_after_deal_damage()

    def check_projectiles_collisions(self, weapon):
        for projectile in weapon.projectiles[:]:
            if not projectile.active:
                continue

            projectile.update()

            if projectile.target.active and projectile.is_collision():
                damage = projectile.damage
                self.deal_damage(enemy=projectile.target, damage=damage)
                projectile.active = False
                weapon.bullets.remove(projectile)

    def deal_damage_to_enemies(self, enemies: list[Enemy], weapon) -> None:
        for enemy in enemies:
            self.deal_damage(enemy=enemy, damage=weapon.get_damage())

    def deal_damage(self, enemy, damage):
        is_critical = random.random() < 0.1
        if is_critical:
            damage *= 1.5

        if enemy.take_damage(int(damage), self.game, is_critical):
            self.game.enemy_died(enemy)
