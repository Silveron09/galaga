import pygame
from os import path

from settings import BLACK

# Указываем путь к папке с ресурсами
image_directory = path.join(path.dirname(__file__), "resources/img")
sound_directory = path.join(path.dirname(__file__), "resources/snd")


# resources.py
# Функции для загрузки ресурсов

def load_image(file_name):
    """ Загрузить изображение из папки с ресурсами. """
    return pygame.image.load(path.join(image_directory, file_name)).convert()


def load_sound(file_name):
    """ Загрузить звук из папки с ресурсами. """
    return pygame.mixer.Sound(path.join(sound_directory, file_name))


# Функции для загрузки конкретных ресурсов игры

def load_player_image():
    return load_image("playerShip1_orange.png")


def load_bullet_image():
    return load_image("laserRed16.png")


def load_meteor_images():
    meteor_list = ["meteorBrown_tiny2.png", "meteorBrown_tiny1.png", "meteorBrown_small2.png",
                   "meteorBrown_small1.png", "meteorBrown_med3.png", "meteorBrown_med1.png",
                   "meteorBrown_big4.png", "meteorBrown_big3.png", "meteorBrown_big2.png",
                   "meteorBrown_big1.png", "meteorGrey_big1.png", "meteorGrey_big2.png",
                   "meteorGrey_big3.png", "meteorGrey_big4.png", "meteorGrey_med1.png",
                   "meteorGrey_med2.png", "meteorGrey_small1.png", "meteorGrey_small2.png",
                   "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]
    return [load_image(img) for img in meteor_list]


def load_powerup_images():
    return {
        "shield": load_image("pill_red.png"),
        "gun": load_image("things_bronze.png")
    }


def load_explosion_anim():
    explosion_anim = {"lg": [], "sm": [], "player": []}
    for i in range(9):
        img_lg = load_image(f"regularExplosion0{i}.png")
        img_lg.set_colorkey(BLACK)
        explosion_anim["lg"].append(pygame.transform.scale(img_lg, (75, 75)))

        img_sm = load_image(f"regularExplosion0{i}.png")
        img_sm.set_colorkey(BLACK)
        explosion_anim["sm"].append(pygame.transform.scale(img_sm, (32, 32)))

        img_player = load_image(f"sonicExplosion0{i}.png")
        img_player.set_colorkey(BLACK)
        explosion_anim["player"].append(img_player)
    return explosion_anim


# Загрузка звуков
def load_game_sounds():
    return {
        "shoot": load_sound("Classik piu.wav"),
        "shield": load_sound("Hil 1.wav"),
        "power": load_sound("Power up 1.wav"),
        "explosion": [load_sound(f"Boom {i}.wav") for i in range(1, 4)],
        "background_music": load_sound("tgfcoder-FrozenJam-SeamlessLoop.ogg")
    }


def load_background():
    """ Загрузить фоновое изображение из папки с ресурсами. """
    # Например, файл фона называется 'starfield.png'.
    return load_image("starfield.png")


def load_player_mini_image():
    """ Загрузить уменьшенное изображение игрока из папки с ресурсами. """
    # Например, уменьшенное изображение игрока называется 'playerShip1_orange_small.png'.
    # Если у вас нет уменьшенного изображения, можете масштабировать основное.
    player_image = load_image("playerShip1_orange.png")
    return pygame.transform.scale(player_image, (25, 19))  # Измените размеры по необходимости

