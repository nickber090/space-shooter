import pygame
import sys
import os
import random
import time


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
                return
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

# Инициализация Pygame
pygame.init()

# Установим размеры окна
size = width, height = 900, 400
screen = pygame.display.set_mode(size)

# Зададим заголовок окна
pygame.display.set_caption("Cosmos Background")

# Загрузим изображение
try:
    background = pygame.image.load('data/cosmos.png').convert()

except pygame.error:
    print("Не удалось загрузить изображение. Проверьте наличие файла cosmos.png.")
    pygame.quit()
    sys.exit()


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


last_meteor_time = time.time()
meteor_creation_interval = 9


class Spaceship(pygame.sprite.Sprite):
    spaceship_image = load_image('spaceship.png', colorkey=(255, 255, 255))

    def __init__(self, group):
        super().__init__(group)
        self.image = Spaceship.spaceship_image
        self.image = pygame.transform.scale(Spaceship.spaceship_image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed = 3

    def update(self):
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


# Основной игровой цикл
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

meteor = Meteorites(all_sprites)

spaceship = Spaceship(all_sprites)

main_menu()
# Основной игровой цикл
main_menu()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    current_time = time.time()
    if current_time - last_meteor_time >= meteor_creation_interval:
        num_meteors = random.randint(1, 2)
        for _ in range(num_meteors):
            Meteorites(all_sprites)  # Создаем новые метеориты
        last_meteor_time = current_time

    # Отображаем фон
    screen.blit(background, (0, 0))

    # Обновляем и рисуем спрайты
    all_sprites.update()
    all_sprites.draw(screen)

    # Обновляем экран
    pygame.display.flip()
    clock.tick(70)

# Завершение Pygame
pygame.quit()
