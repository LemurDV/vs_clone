from entities.entity import Entity
from settings import BLUE, EXP_ORB_RADIUS, EXP_ORB_SPEED, pygame


class ExperienceOrb(Entity):
    """Сфера опыта"""

    def __init__(self, x, y, value):
        super().__init__(
            x=x,
            y=y,
            width=20,
            height=20,
            color=BLUE,
            radius=EXP_ORB_RADIUS,
            speed=EXP_ORB_SPEED,
        )
        self.value = value
        self.sprite = pygame.image.load(
            "assets/items/exp_orb.jpg"
        ).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (20, 20))

    def update(self, game):
        """Обновление сферы опыта"""
        player = game.player
        if player and player.active:
            distance = self.distance_to(player)

            if distance < player.magnet_radius:
                # Движение к игроку
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery

                if distance > 0:
                    dx = (dx / distance) * self.speed
                    dy = (dy / distance) * self.speed
                    self.move(dx, dy)

            # Проверка сбора
            if self.check_collision(player):
                player.add_experience(self.value)
                self.destroy()

    def draw(self, screen):
        """Отрисовка сферы опыта"""
        # pygame.draw.circle(
        #     screen, self.color, self.rect.center, self.rect.width // 2
        # )
        screen.blit(self.sprite, self.rect)
        # pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
