import pygame
import sys
import os
import random
import time


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
    fon = pygame.transform.scale(pygame.image.load('data/intro_fon.jpg'), size)
    font = pygame.font.Font(None, 35)
    screen.blit(fon, (0, 0))
    games_title = font.render("Space-shooter", 1, pygame.Color('white'))
    str_rect = games_title.get_rect()
    str_rect.x = width // 2 - str_rect.width // 2
    str_rect.top = 20
    screen.blit(games_title, str_rect)
    instruction = font.render("Чтобы начать игру, нажмите любую кнопку.", 1, pygame.Color('white'))
    str_rect = instruction.get_rect()
    str_rect.x = 175
    str_rect.top = 175
    screen.blit(instruction, str_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                main_cycle()
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
                main_cycle()
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


def main_cycle():
    restart_game()
    running = True
    last_meteor_time = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
        current_time = time.time()
        if current_time - last_meteor_time >= meteor_creation_interval:
            num_meteors = random.randint(1, 2)
            for _ in range(num_meteors):
                m = Meteorites(all_sprites)  # Создаем новые метеориты
                all_meteorites.add(m)
            last_meteor_time = current_time

        # Отображаем фон
        screen.blit(background, (0, 0))

        # Обновляем и рисуем спрайты
        all_sprites.update()
        all_sprites.draw(screen)

        # Обновляем экран
        pygame.display.flip()
        clock.tick(70)


def restart_game():
    all_sprites.empty()
    all_meteorites.empty()
    spaceship = Spaceship(all_sprites)
    meteor = Meteorites(all_sprites)
    all_meteorites.add(meteor)


class Meteorites(pygame.sprite.Sprite):
    image = load_image("meteor.png", -1)  # Указываем colorkey

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
        self.rect.x = width + random.randint(0, width // 2)

    def update(self):
        self.rect.x -= self.speed  # Движение справа на лево
        if self.rect.right < 0:
            self.reset_pos()


meteor_creation_interval = 9


class Spaceship(pygame.sprite.Sprite):
    spaceship_image = load_image('spaceship.png', colorkey=(255, 255, 255))
    health_point = 100

    def __init__(self, group):
        super().__init__(group)
        self.image = Spaceship.spaceship_image
        self.image = pygame.transform.scale(Spaceship.spaceship_image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed = 3
        self.health_point = Spaceship.health_point

    def update(self):
        if self.health_point <= 0:
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
    full_hp_image = None
    half_hp_image = None
    zero_hp_image = None

    def __init__(self, group):
        super.__init__(group)
        self.image = HealthPoints.full_hp_image



if __name__ == '__main__':
    main_menu()
