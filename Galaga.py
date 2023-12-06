#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
# Art from Kenney.nl

import pygame
import random
from os import path
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

#Обозначение цветов
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#включаем Пайгейм и создаем окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Mission") #Устанавливаем название для игры
clock = pygame.time.Clock()

font_name = pygame.font.match_font("arial") # Задаем шрифт
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect() # Хитбокс текста
    text_rect.midtop=(x, y)
    surf.blit(text_surface,text_rect) #отображение поверхности

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.shield = 100
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38)) #Скелим (меняем размер)
        self.image.set_colorkey(BLACK) #Задаем изначальный цвет на который наложим картинку
        self.rect = self.image.get_rect() #Задаем обьем
        self.rect.centerx = WIDTH / 2 #Задаем центр обьекта
        self.rect.bottom = HEIGHT - 10 #Задаем низ обьекта
        self.speedx = 0 #Задаем изначальную скорость обьекту
        self.radius = 20
        self.shoot_delay = 150 #Задаем скорость в кадрах
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2 #Задаем центр обьекта
            self.rect.bottom = HEIGHT - 10 #Задаем низ обьекта
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]: #Управление на стрелочках влево
            self.speedx = -5 #Скорость передвижения
        if keystate[pygame.K_RIGHT]: #Управление на стрелочках вправо
            self.speedx = 5 #Скорость передвижения
        if keystate[pygame.K_SPACE]: #Управление на пробел
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <0:
            self.rect.left = 0

    def hide(self):
        #временно убираем игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()
class Mob(pygame.sprite.Sprite): #Создаем моба
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(2, 6) #Скорость падения мобов
        self.speedx = random.randrange(-3, 3) #Скорость отклонения по сторонам мобов
        self.radius = int(self.rect.width * .9 / 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 40 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(2, 6)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self): #Придаем свойства (настройки, управление)
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "gun"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self): #Придаем свойства (настройки, управление)
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Galaga", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "<- -> Движение, Пробел стрелять", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Нажмите любую клавишу чтобы начать", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

    #Загружаем модельки
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()  #Фон
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert() # Игрок
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()  #Пуля
meteor_images = []
meteor_list = ["meteorBrown_tiny2.png", "meteorBrown_tiny1.png", "meteorBrown_small2.png", "meteorBrown_small1.png", "meteorBrown_med3.png",
               "meteorBrown_med1.png", "meteorBrown_big4.png", "meteorBrown_big3.png", "meteorBrown_big2.png", "meteorBrown_big1.png",
               "meteorGrey_big1.png", "meteorGrey_big2.png", "meteorGrey_big3.png", "meteorGrey_big4.png", "meteorGrey_med1.png",
               "meteorGrey_med2.png", "meteorGrey_small1.png", "meteorGrey_small2.png", "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"] #список всех изображений
for img in meteor_list:
    meteor_images.append(pygame.image.load (path.join(img_dir, img)).convert())

powerup_images = {}
powerup_images["gun"] = pygame.image.load(path.join(img_dir, "things_bronze.png")).convert() #
powerup_images["shield"] = pygame.image.load(path.join(img_dir, "pill_red.png")).convert() #

explosion_anim = {} # СЛОВАРЬ С МАССИВОМ КАРТИНОК
explosion_anim["lg"] = [] #бОЛЬШОЙ взрыв
explosion_anim["sm"] = [] #Маленький взрыв
explosion_anim["player"] = [] #взрыв(игрок)
for i in range(9):
    filename = f"regularExplosion0{i}.png".format()
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK) #Изначальный цвет
    img_lg = pygame.transform.scale(img, (75, 75)) #Размер взрыва(Большой)
    explosion_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32)) #Размер взрыва(маленький)
    explosion_anim["sm"].append(img_sm)
    filename = f"sonicExplosion0{i}.png".format()
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK) #Изначальный цвет
    explosion_anim["player"].append(img)


shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "Classik piu.wav"))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, "Hil 1.wav"))
power_sound = pygame.mixer.Sound(path.join(snd_dir, "Power up 1.wav"))
expl_sounds = []
for snd in ["Boom 3.wav", "Boom 2.wav", "Boom 1.wav"]:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, "tgfcoder-FrozenJam-SeamlessLoop.ogg")) #Музыка на фоне
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops= -1)

#Создаем цикл игры
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8): #Число мобов
            newmob()
        score = 0
    #поддерживаем цикл на нужной скорости
    clock.tick(FPS)
    #Создаем инпуты (ивенты)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Обновление
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) # Попадание по мобу
    for hit in hits:
        score += 50 - hit.radius
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, "lg")
        all_sprites.add(expl)
        newmob()

    hits = pygame.sprite.spritecollide(player, powerups, True) #
    for hit in hits: #если попадет
        if hit.type == "shield":
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == "gun":
            player.powerup()
            power_sound.play()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) #попадание по игроку
    for hit in hits: #если попадет
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, "sm")
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion (player.rect.center, "player")
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    #Отрисовываем/Рендерим
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
# ПОСЛЕ отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()