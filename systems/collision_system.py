import random


class CollisionSystem:
    def __init__(self, game):
        self.game = game

    def update(self):
        for weapon in self.game.player.weapons.values():
            if weapon.can_attack():
                for enemy in self.game.enemy_manager.enemies[:]:
                    if weapon.is_collision(enemy=enemy):
                        damage = weapon.get_damage()
                        self.deal_damage(enemy=enemy, damage=damage)
                        weapon.action_after_deal_damage()

    def deal_damage(self, enemy, damage):
        is_critical = random.random() < 0.1
        if is_critical:
            damage *= 2

        if enemy.take_damage(damage, self.game, is_critical):
            self.game.enemy_died(enemy)