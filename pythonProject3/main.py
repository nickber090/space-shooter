import pygame
import sys
import os
import random
import time

from pygame.examples.cursors import image

# Инициализация Pygame
pygame.init()

# Установим размеры окна
size = width, height = 900, 400
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
background = pygame.image.load('data/cosmos.png').convert()

# Зададим заголовок окна
pygame.display.set_caption("Space-shooter")

all_sprites = pygame.sprite.Group()
all_meteorites = pygame.sprite.Group()


def main_menu():
    second_lvl = False
    third_lvl = False
    with open('levels') as f:
        data = f.read()
        if data[0] == '1':
            second_lvl = True
        if data[1] == '1':
            third_lvl = True

    fon = pygame.transform.scale(pygame.image.load('data/intro_fon.jpg'), size)
    font = pygame.font.Font(None, 35)
    screen.blit(fon, (0, 0))

    games_title = font.render("Space-shooter", 1, pygame.Color('white'))
    title_rect = games_title.get_rect()
    title_rect.x = width // 2 - title_rect.width // 2
    title_rect.top = 20
    screen.blit(games_title, title_rect)

    f_lvl = font.render('Уровень 1', 1, pygame.Color('white'))
    f_lvl_rect = f_lvl.get_rect()
    f_lvl_rect.x = width // 3 - f_lvl.get_width()
    f_lvl_rect.top = height // 2 - f_lvl.get_height() // 2
    screen.blit(f_lvl, f_lvl_rect)

    if second_lvl:
        s_lvl = font.render('Уровень 2', 1, pygame.Color('white'))
        s_lvl_rect = s_lvl.get_rect()
        s_lvl_rect.x = width // 2 - s_lvl.get_width() // 2
        s_lvl_rect.top = height // 2 - s_lvl.get_height() // 2
        screen.blit(s_lvl, s_lvl_rect)

    if third_lvl:
        th_lvl = font.render('Уровень 3', 1, pygame.Color('white'))
        th_lvl_rect = th_lvl.get_rect()
        th_lvl_rect.x = 2 * width // 3
        th_lvl_rect.top = height // 2 - th_lvl.get_height() // 2
        screen.blit(th_lvl, th_lvl_rect)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and f_lvl_rect.colliderect(pygame.Rect(*event.pos, 10, 10)):
                first_level()
            if (second_lvl and event.type == pygame.MOUSEBUTTONDOWN
                    and s_lvl_rect.colliderect(pygame.Rect(*event.pos, 10, 10))):
                seconds_level()
            if (third_lvl and event.type == pygame.MOUSEBUTTONDOWN
                    and th_lvl_rect.colliderect(pygame.Rect(*event.pos, 10, 10))):
                pass
        pygame.display.flip()


def death_screen():
    fon = pygame.transform.scale(pygame.image.load('data/death_screen.PNG'), size)
    font = pygame.font.Font(None, 35)
    screen.blit(fon, (0, 0))
    main_menu_button = font.render('Главное меню', 1, pygame.Color('white'))
    main_menu_btn_rect = main_menu_button.get_rect()
    main_menu_btn_rect.x = width // 2 - main_menu_btn_rect.width // 2
    main_menu_btn_rect.top = height // 100 * 80
    screen.blit(main_menu_button, main_menu_btn_rect)
    continue_button = font.render('Продолжить', 1, pygame.Color('white'))
    continue_btn_rect = continue_button.get_rect()
    continue_btn_rect.x = width // 2 - continue_btn_rect.width // 2
    continue_btn_rect.top = height // 100 * 65
    screen.blit(continue_button, continue_btn_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and continue_btn_rect.colliderect(pygame.Rect(*event.pos, 10, 10)):
                first_level()
            if event.type == pygame.MOUSEBUTTONDOWN and main_menu_btn_rect.colliderect(pygame.Rect(*event.pos, 10, 10)):
                main_menu()
        pygame.display.flip()


def victory_screen():
    fon = pygame.transform.scale(pygame.image.load('data/victory_screen.PNG'), size)
    font = pygame.font.Font(None, 35)
    screen.blit(fon, (0, 0))
    main_menu_button = font.render('Главное меню', 1, pygame.Color('white'))
    main_menu_btn_rect = main_menu_button.get_rect()
    main_menu_btn_rect.x = width // 2 - main_menu_btn_rect.width // 2 - 10
    main_menu_btn_rect.top = height // 100 * 65
    screen.blit(main_menu_button, main_menu_btn_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and main_menu_btn_rect.colliderect(pygame.Rect(*event.pos, 10, 10)):
                main_menu()
        pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def first_level():
    restart_game()
    spaceship = Spaceship(all_sprites)
    hp = HealthPoints(all_sprites)
    running = True
    last_meteor_time = time.time()
    game_time = 50
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('arial', 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.USEREVENT:
                game_time -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
        current_time = time.time()
        if current_time - last_meteor_time >= meteor_creation_interval:
            num_meteors = random.randint(1, 2)
            for _ in range(num_meteors):
                m = Meteorites(all_sprites)  # Создаем новые метеориты
                all_meteorites.add(m)
            last_meteor_time = current_time
        if spaceship.health_point <= 50:
            hp.image = HealthPoints.half_hp_image

        # Отображаем фон
        screen.blit(background, (0, 0))
        text = font.render(str(game_time), True, pygame.Color('red'))
        screen.blit(text, (width // 2 - text.get_width() // 2, text.get_height() // 2))
        # проверка на то, закончилось ли время. если да, то уровень пройден,
        # и в файл с уровнями записывается 1 вместо первого 0 для открытия 2-ого уровня
        if game_time == 0:
            with open('levels') as f:
                data = list(f.read())
                data[0] = '1'
            with open('levels', 'w') as f:
                f.write(''.join(data))
            victory_screen()

        # Обновляем и рисуем спрайты
        all_sprites.update()
        all_sprites.draw(screen)

        # Обновляем экран
        pygame.display.flip()
        clock.tick(70)


def seconds_level():
    restart_game_s_level()
    spaceship = Spaceship(all_sprites)
    hp = HealthPoints(all_sprites)
    running = True
    game_time = 50
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('arial', 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.USEREVENT:
                game_time -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
        if spaceship.health_point <= 50:
            hp.image = HealthPoints.half_hp_image

        # Отображаем фон
        screen.blit(background, (0, 0))
        text = font.render(str(game_time), True, pygame.Color('red'))
        screen.blit(text, (width // 2 - text.get_width() // 2, text.get_height() // 2))
        # проверка на то, закончилось ли время. если да, то уровень пройден,
        # и в файл с уровнями записывается 1 вместо первого 0 для открытия 2-ого уровня
        if game_time == 0:
            with open('levels') as f:
                data = list(f.read())
                data[1] = '1'
            with open('levels', 'w') as f:
                f.write(''.join(data))
            victory_screen()

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(70)

def restart_game_s_level():
    all_sprites.empty()



def restart_game():
    all_sprites.empty()
    all_meteorites.empty()
    meteor = Meteorites(all_sprites)
    all_meteorites.add(meteor)


class Meteorites(pygame.sprite.Sprite):
    image = load_image("meteor.png", -1) # Указываем colorkey

    def __init__(self, group):
        super().__init__(group)
        self.image = Meteorites.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.speed = 2
        self.reset_pos()

    def reset_pos(self):
        self.rect.y = random.randint(0, height - self.rect.height)
        self.rect.x = width + random.randint(0, 65)

    def update(self):
        self.rect.x -= self.speed  # Движение справа на лево
        if self.rect.right < 0:
            self.reset_pos()


meteor_creation_interval = 9


class Spaceship(pygame.sprite.Sprite):
    spaceship_image = load_image('spaceship.png', colorkey=(255, 255, 255))
    image_boom = load_image("boom.png")
    health_point = 100

    def __init__(self, group):
        super().__init__(group)
        self.image = Spaceship.spaceship_image
        self.imageb = Spaceship.image_boom
        self.imageb = pygame.transform.scale(Spaceship.image_boom, (120, 120))
        self.image = pygame.transform.scale(Spaceship.spaceship_image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed = 3
        self.health_point = Spaceship.health_point
        self.dead = False
        self.boom_time = 0

    def update(self, *args):
        if self.health_point <= 0 and not self.dead:
            self.image = self.imageb
            self.dead = True
            self.boom_time = pygame.time.get_ticks()
            self.speed = 0

        if self.dead and pygame.time.get_ticks() - self.boom_time > 600:
            time.sleep(0.5)
            death_screen()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Ограничиваем движение корабля экраном
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(width, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(height, self.rect.bottom)

        if pygame.sprite.spritecollide(self, all_meteorites, True):
            self.health_point -= 50


class HealthPoints(pygame.sprite.Sprite):
    full_hp_image = load_image('full_hp.png', -1)
    full_hp_image = pygame.transform.scale(full_hp_image, (50, 50))
    half_hp_image = load_image('half_hp.png', -1)
    half_hp_image = pygame.transform.scale(half_hp_image, (50, 50))

    def __init__(self, group):
        super().__init__(group)
        self.image = HealthPoints.full_hp_image
        self.rect = self.image.get_rect()
        self.rect.x = self.image.get_width() // 4
        self.rect.y = self.image.get_height() // 4


if __name__ == '__main__':
    main_menu()
