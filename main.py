import pygame

from config import (
    HEIGHT,
    WIDTH,
)
from game import Game
from main_menu import MainMenu


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Vampire Survivors Clone")

    # менюшка
    menu = MainMenu(screen)
    selected_level = menu.run()

    if selected_level is not None:
        game = Game(selected_level)
        game.run()

    pygame.quit()
