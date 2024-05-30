import pygame

from settings import WHITE, RED, BLACK, WIDTH, HEIGHT, FPS


# game_functions.py
def draw_text(surf, text, size, x, y, font_name):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()  # Хитбокс текста
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)  # отображение поверхности


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


def show_go_screen(screen, background, background_rect, font_name, clock):
    screen.blit(background, background_rect)
    draw_text(screen, "Galaga", 64, WIDTH / 2, HEIGHT / 4, font_name)
    draw_text(screen, "<- -> Движение, Пробел стрелять", 22, WIDTH / 2, HEIGHT / 2, font_name)
    draw_text(screen, "Нажмите любую клавишу чтобы начать", 18, WIDTH / 2, HEIGHT * 3 / 4, font_name)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYUP:
                return True
