import pygame

from settings import WIDTH
from src.utils.game_functions import draw_text


class ScoreManager:
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.font_name = pygame.font.match_font('arial')

    def update_score(self):
        # Обновление и логика очков
        pass

    def draw_score(self):
        draw_text(self.game.screen, str(self.score), 18, WIDTH / 2, 10, self.font_name)

    def reset_score(self):
        self.score = 0