import pygame

from game import Game


def main():
    """Основная функция"""
    pygame.init()
    pygame.display.set_caption("Vampire Survivors Clone")

    game = Game()
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
