import pygame

from resources import load_game_sounds
from settings import WIDTH, FPS, BLACK, HEIGHT
from src.managers.collision_handler import CollisionHandler
from src.managers.entity_manager import EntityManager
from src.managers.resource_manager import ResourceManager
from src.managers.score_manager import ScoreManager
from src.utils.game_functions import draw_text, draw_shield_bar, draw_lives, show_go_screen


class Game:
    def __init__(self):
        pygame.init()
        self.font_name = pygame.font.match_font('arial')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Mission")
        self.clock = pygame.time.Clock()
        self.collision_handler = CollisionHandler(self)
        self.score_manager = ScoreManager(self)
        self.resource_manager = ResourceManager()
        self.entity_manager = EntityManager(self.resource_manager)
        self.running = True
        self.game_over = True
        self.game_sounds = load_game_sounds()
        self.background = self.resource_manager.background
        self.background_rect = self.resource_manager.background_rect

    def run(self):
        while self.running:
            # Ограничение частоты кадров
            self.clock.tick(FPS)
            self.processing_game_over()
            self.update_game()
            # Обработка выхода при нажатии на крест
            self.handle_exit()

    def processing_game_over(self):
        if self.game_over:
            # Показ начального экрана
            self.running = show_go_screen(self.screen, self.resource_manager.background,
                                          self.resource_manager.background_rect,
                                          self.font_name, self.clock)
            # После завершения начального экрана сбрасываем состояние игры
            self.game_over = not self.running
            self.reset_game()

    def update_game(self):
        # Обновление состояний всех игровых сущностей
        self.entity_manager.update_entities()
        # Проверка и обработка столкновений
        self.collision_handler.check_collisions()
        # Обновление игрового счёта и связанных с ним данных
        self.score_manager.update_score()
        # Отрисовка всех элементов игры на экране
        self.draw()

    def stop_music(self):
        for sound in self.game_sounds.values():
            if isinstance(sound, list):
                for s in sound:
                    s.stop()
            else:
                sound.stop()

    def handle_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_music()
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.resource_manager.background, self.resource_manager.background_rect)
        self.entity_manager.all_sprites.draw(self.screen)
        # Использование вспомогательных функций для отображения информации
        draw_text(self.screen, f"Score: {self.score_manager.score}", 18, WIDTH / 2, 10, self.font_name)
        draw_shield_bar(self.screen, 5, 5, self.entity_manager.player.shield)
        draw_lives(self.screen, WIDTH - 100, 5, self.entity_manager.player.lives, self.resource_manager.player_mini_img)

        # self.score_manager.draw_score()
        pygame.display.flip()

    def reset_game(self):
        self.entity_manager.reset_entities()
        self.score_manager.reset_score()
