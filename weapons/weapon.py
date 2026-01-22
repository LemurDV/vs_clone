from loguru import logger

class Weapon:
    def __init__(self, name, damage, cooldown, owner):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown  # в миллисекундах!
        self.owner = owner  # Ссылка на игрока
        self.last_attack = 0
        self.level = 1
        self.max_level = 6  # Максимальный уровень для баланса

    def update(self, current_time, enemies):
        """Обновление оружия - должен быть переопределен"""
        pass

    def draw(self, screen):
        """Отрисовка оружия - должен быть переопределен"""
        pass

    def level_up(self, player_dmg):
        """Улучшение оружия"""
        if self.level < self.max_level:
            self.level += 1
            # self.damage = int(self.damage * 1.2)  # +20% урона за уровень
            self.damage = self.damage + int(player_dmg * 0.2)
            logger.debug(f"{self.damage=}")
            return True
        return False  # Достигнут максимальный уровень
