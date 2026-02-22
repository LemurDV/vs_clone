import random

from entities import Enemy
from systems.effect_manager import EffectManager
from weapons.lightning_ball_weapon import LightningBallWeapon
from weapons.magic_bullet_weapon import MagicBulletWeapon
from weapons.scythe import ScytheWeapon


class CollisionSystem:
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.effect_manager = EffectManager()

    def update(self):
        for weapon in self.game.player.weapons.values():
            if weapon.can_attack():
                if weapon.weapon_type == "aura":
                    self.aura_weapon_actions(weapon)
                elif weapon.weapon_type == "projectile":
                    self.projectile_weapon_actions(weapon)
                elif weapon.weapon_type == "melee":
                    self.melee_weapon_actions(weapon)
                elif weapon.weapon_type == "beam":
                    self.beam_weapon_actions(weapon)

            if weapon.hit_enemies:
                self.deal_damage_to_enemies(
                    enemies=weapon.hit_enemies,
                    weapon=weapon,
                )
                self.actions_after_deal_damage(weapon=weapon)

    def aura_weapon_actions(self, weapon):
        for enemy in self.game.enemy_manager.active_enemies[:]:
            if weapon.is_collision(enemy=enemy):
                weapon.add_enemy_to_hit(enemy=enemy)

    def projectile_weapon_actions(
        self, weapon: MagicBulletWeapon | LightningBallWeapon
    ):
        weapon.shoot(self.game.enemy_manager.enemies)
        self.check_projectiles_collisions(weapon=weapon)

    def check_projectiles_collisions(
        self, weapon: MagicBulletWeapon | LightningBallWeapon
    ):
        for projectile in weapon.projectiles[:]:
            if not projectile.active:
                continue

            projectile.update()

            if projectile.target.active and projectile.is_collision():
                damage = projectile.damage
                self.deal_damage(enemy=projectile.target, damage=damage)
                weapon.remove_enemy_from_list(enemy=projectile.target)
                projectile.active = False
                weapon.projectiles.remove(projectile)

    def melee_weapon_actions(self, weapon: ScytheWeapon):
        active_enemies = self.game.enemy_manager.active_enemies
        weapon.shoot(active_enemies=active_enemies, game=self.game)
        weapon.detect_enemies_in_range(
            enemies=active_enemies,
            direction=weapon.attack_direction,
        )

    def beam_weapon_actions(self, weapon):
        weapon.shoot(self.game)

    def actions_after_deal_damage(self, weapon):
        if self.player.vampire and weapon.len_hit_enemies > 0:
            self.make_vampire(weapon=weapon)
        weapon.action_after_deal_damage()
        weapon.reset_hit_enemies()

    def make_vampire(self, weapon):
        total_vampire = weapon.len_hit_enemies * self.player.vampire
        self.player.heal(total_vampire)
        self.game.particle_system.add_heal_text(
            x=self.player.x,
            y=self.player.y,
            heal=total_vampire,
        )

    def deal_damage_to_enemies(self, enemies: list[Enemy], weapon) -> None:
        for enemy in enemies:
            self.deal_damage(enemy=enemy, damage=weapon.get_damage())
            self.apply_weapon_effects(enemy, weapon)

    def deal_damage(self, enemy, damage):
        is_critical = random.random() < self.player.critical_chance
        if is_critical:
            damage *= 1.5

        if enemy.take_damage(int(damage), self.game, is_critical):
            self.game.enemy_died(enemy)

    def apply_weapon_effects(self, enemy: Enemy, weapon):
        if weapon.causes_bleeding_chance:
            if random.random() < weapon.causes_bleeding_chance:
                effect = self.effect_manager.create_bleed_effect(
                    source_weapon=weapon,
                )
                enemy.apply_effect(effect)

        if weapon.causes_burn_chance:
            if random.random() < weapon.causes_burn_chance:
                effect = self.effect_manager.create_burn_effect(
                    source_weapon=weapon,
                )
                enemy.apply_effect(effect)

        if weapon.causes_poison_chance:
            if random.random() < weapon.causes_poison_chance:
                effect = self.effect_manager.create_poison_effect(
                    source_weapon=weapon,
                )
                enemy.apply_effect(effect)
