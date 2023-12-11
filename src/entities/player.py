import pygame

from resources import load_player_image, load_game_sounds
from settings import WIDTH, HEIGHT, BLACK, POWERUP_TIME
from src.entities.bullet import Bullet


class Player(pygame.sprite.Sprite):
    MOVE_SPEED = 5
    HIDE_TIME = 1000
    POWERUP_TIME = 5000  # Пример времени для power-up

    def __init__(self, all_sprites, bullets):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(load_player_image(), (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 150
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        # Добавлены атрибуты для управления спрайтами и звуками
        self.all_sprites = all_sprites
        self.bullets = bullets
        self.shoot_sound = load_game_sounds()["shoot"]

        @property
        def shield(self):
            return self._shield

        @shield.setter
        def shield(self, value):
            self._shield = max(0, min(100, value))  # Ограничиваем значение между 0 и 100

        @property
        def power(self):
            return self._power

        @power.setter
        def power(self, value):
            self._power = max(1, value)  # Минимальная сила - 1

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2  # Задаем центр объекта
            self.rect.bottom = HEIGHT - 10  # Задаем низ объекта

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        movement = {pygame.K_LEFT: -self.MOVE_SPEED, pygame.K_RIGHT: self.MOVE_SPEED}
        for key in movement:
            if keystate[key]:
                self.speedx = movement[key]

        if keystate[pygame.K_SPACE]:  # Управление на пробел
            self.shoot()

        self.rect.x += self.speedx
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))  # Ограничиваем движение в пределах экрана

    def hide(self):
        # временно убираем игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self._create_bullets()

    def _create_bullets(self):
        if self.power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)
        elif self.power == 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            self.all_sprites.add(bullet1)
            self.all_sprites.add(bullet2)
            self.bullets.add(bullet1)
            self.bullets.add(bullet2)
        else:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            bullet3 = Bullet(self.rect.centerx, self.rect.top)
            self.all_sprites.add(bullet1)
            self.all_sprites.add(bullet2)
            self.all_sprites.add(bullet3)
            self.bullets.add(bullet1)
            self.bullets.add(bullet2)
            self.bullets.add(bullet3)

        self.shoot_sound.play()


