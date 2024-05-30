import random

import pygame

from resources import load_game_sounds
from src.entities.explosion import Explosion
from src.entities.pow import Pow


class CollisionHandler:
    EXPLOSION_SIZE = 'lg'
    PLAYER_EXPLOSION_SIZE = 'player'
    SHIELD_POWERUP_CHANCE = 0.9
    SHIELD_INCREASE = random.randrange(10, 30)
    MAX_SHIELD = 100

    def __init__(self, game):
        self.game = game
        self.sounds = load_game_sounds()

    def check_collisions(self):
        self.check_mob_bullet_collisions()
        self.check_powerup_collisions()
        self.check_mob_player_collisions()

    def check_mob_bullet_collisions(self):
        hits = pygame.sprite.groupcollide(
            self.game.entity_manager.mobs,
            self.game.entity_manager.bullets,
            True, True
        )
        for hit in hits:
            self.game.score_manager.score += 50 - hit.radius
            self.handle_mob_hit(hit)

    def handle_mob_hit(self, mob):
        if random.random() > self.SHIELD_POWERUP_CHANCE:
            self.create_powerup(mob.rect.center)

        random.choice(self.sounds["explosion"]).play()
        self.create_explosion(mob.rect.center, self.EXPLOSION_SIZE)
        self.game.entity_manager.new_mob()

    def check_powerup_collisions(self):
        hits = pygame.sprite.spritecollide(
            self.game.entity_manager.player,
            self.game.entity_manager.powerups,
            True
        )
        for hit in hits:
            self.handle_powerup_hit(hit)

    def handle_powerup_hit(self, powerup):
        if powerup.type == "shield":
            self.game.entity_manager.player.shield += self.SHIELD_INCREASE
            self.sounds["shield"].play()
            if self.game.entity_manager.player.shield > self.MAX_SHIELD:
                self.game.entity_manager.player.shield = self.MAX_SHIELD
        elif powerup.type == "gun":
            self.game.entity_manager.player.powerup()
            self.sounds["power"].play()

    def check_mob_player_collisions(self):
        hits = pygame.sprite.spritecollide(
            self.game.entity_manager.player,
            self.game.entity_manager.mobs,
            True,
            pygame.sprite.collide_circle
        )
        for hit in hits:
            self.handle_player_hit(hit)

    def handle_player_hit(self, hit):
        self.game.entity_manager.player.shield -= hit.radius * 2
        self.create_explosion(hit.rect.center, self.PLAYER_EXPLOSION_SIZE)
        self.game.entity_manager.new_mob()
        if self.game.entity_manager.player.shield <= 0:
            self.game_over_sequence()

    def game_over_sequence(self):
        self.create_explosion(self.game.entity_manager.player.rect.center, self.PLAYER_EXPLOSION_SIZE)
        self.game.entity_manager.player.hide()
        self.game.entity_manager.player.lives -= 1
        self.game.entity_manager.player.shield = self.MAX_SHIELD
        if self.game.entity_manager.player.lives <= 0:
            self.game.game_over = True

    def create_explosion(self, center, size):
        explosion = Explosion(center, size)
        self.game.entity_manager.all_sprites.add(explosion)

    def create_powerup(self, center):
        powerup = Pow(center)
        self.game.entity_manager.powerups.add(powerup)
        self.game.entity_manager.all_sprites.add(powerup)
