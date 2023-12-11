from os import path

import pygame

from resources import (sound_directory,
                       load_player_image, load_meteor_images, load_powerup_images,
                       load_explosion_anim, load_game_sounds, load_player_mini_image, load_image)


def background_music():
    # Загрузка фоновой музыки
    pygame.mixer.music.load(path.join(sound_directory, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1)


class ResourceManager:
    def __init__(self):
        # Загрузка всех ресурсов
        self.background = load_image("starfield.png")
        self.player_img = load_player_image()
        self.meteor_images = load_meteor_images()
        self.powerup_images = load_powerup_images()
        self.explosion_anim = load_explosion_anim()
        self.sounds = load_game_sounds()
        self.player_mini_img = load_player_mini_image()
        self.background_rect = self.background.get_rect()
        background_music()
