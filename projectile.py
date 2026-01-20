from config import (
    HEIGHT,
    PROJECTILE_RADIUS,
    PROJECTILE_SPEED,
    WHITE,
    WIDTH,
    pygame,
)


class Projectile:
    def __init__(self, x, y, dx, dy, damage, color, is_crit=False):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = PROJECTILE_RADIUS
        self.speed = PROJECTILE_SPEED
        self.damage = damage
        self.color = color
        self.is_crit = is_crit
        if is_crit:
            self.color = (255, 255, 0)

    def move(self):
        """Движение снаряда"""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self, screen):
        """Отрисовка снаряда"""
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), self.radius
        )
        # Добавляем небольшой блик для эффекта
        pygame.draw.circle(
            screen, WHITE, (int(self.x), int(self.y)), self.radius // 2
        )

    def is_off_screen(self):
        """Проверка, вышел ли снаряд за пределы экрана"""
        margin = 20
        return (
            self.x < -margin
            or self.x > WIDTH + margin
            or self.y < -margin
            or self.y > HEIGHT + margin
        )

    def check_collision(self, enemy_x, enemy_y, enemy_radius):
        """Проверка столкновения с врагом"""
        dx = enemy_x - self.x
        dy = enemy_y - self.y
        distance = (dx * dx + dy * dy) ** 0.5
        return distance < self.radius + enemy_radius
