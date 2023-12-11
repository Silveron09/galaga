import pygame
from src.entities.player import Player
from src.entities.mob import Mob
from src.entities.pow import Pow


class EntityManager:
    def __init__(self, resource_manager):
        self.player = None
        self.resource_manager = resource_manager
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.create_player()
        self.create_mobs()

    def create_player(self):
        self.player = Player(self.all_sprites, self.bullets)
        self.all_sprites.add(self.player)

    def create_mobs(self):
        for i in range(8):
            mob = Mob()
            self.mobs.add(mob)
            self.all_sprites.add(mob)

    def new_mob(self):
        mob = Mob()
        self.mobs.add(mob)
        self.all_sprites.add(mob)

    def create_powerup(self, center):
        # Создание бонуса и добавление его в соответствующие группы
        powerup = Pow(center)
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)

    def update_entities(self):
        self.all_sprites.update()

    def reset_entities(self):
        self.all_sprites.empty()
        self.mobs.empty()
        self.bullets.empty()
        self.powerups.empty()  # Очистка группы бонусов
        self.create_player()
        self.create_mobs()
