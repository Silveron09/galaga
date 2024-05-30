import pygame

from src.managers.game_manager import Game


def main():
    # Инициализация библиотеки Pygame
    pygame.init()
    pygame.mixer.init()

    # Создание экземпляра игры
    game = Game()

    # Запуск игрового процесса
    game.run()

    # Завершение работы Pygame после выхода из игрового цикла
    pygame.quit()


if __name__ == '__main__':
    main()
