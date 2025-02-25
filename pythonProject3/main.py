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
current_lvl = None


#создание групп для спрайтов
all_sprites = pygame.sprite.Group()
all_meteorites = pygame.sprite.Group()
all_opponents = pygame.sprite.Group()
spaceships = pygame.sprite.Group()
all_meteorites_2 = pygame.sprite.Group()


def main_menu():
    # Проверка на то, прошел ли игрок 1 и 2 уровень
    second_lvl = False
    third_lvl = False
    global current_lvl
    with open('levels') as f:
        data = f.read()
        if data[0] == '1':
            second_lvl = True
        if data[1] == '1':
            third_lvl = True

    fon = pygame.transform.scale(pygame.image.load('data/intro_fon.jpg'), size)
    font = pygame.font.Font(None, 35)
    screen.blit(fon, (0, 0))

    instructions_list = ['Инструкция:', 'Управление кораблём - стрелочки',
                         'Выход в главное меню - Escape', 'Стрельба - пробел']

    # Вывод инструкции в главном меню
    for i in range(1, len(instructions_list) + 1):
        instruction = font.render(instructions_list[i - 1], 1, pygame.Color('white'))
        instruction_rect = instruction.get_rect()
        instruction_rect.x = 10
        instruction_rect.y =  (height // 2 + height // 6) + 25 * i
        screen.blit(instruction, instruction_rect)

    # Название игры
    games_title = font.render("Space-shooter", 1, pygame.Color('white'))
    title_rect = games_title.get_rect()
    title_rect.x = width // 2 - title_rect.width // 2
    title_rect.top = 20
    screen.blit(games_title, title_rect)

    # Кнопка перехода на 1 уровень
    f_lvl = font.render('Уровень 1', 1, pygame.Color('white'))
    f_lvl_rect = f_lvl.get_rect()
    f_lvl_rect.x = width // 3 - f_lvl.get_width()
    f_lvl_rect.top = height // 2 - f_lvl.get_height() // 2
    screen.blit(f_lvl, f_lvl_rect)

    # Кнопка выхода из игры
    exit_button = font.render('Выход', 1, pygame.Color('white'))
    exit_btn_rect = exit_button.get_rect()
    exit_btn_rect.x = width - width // 8
    exit_btn_rect.top = height // 100 * 85
    screen.blit(exit_button, exit_btn_rect)

    # Если игрок прошел 1 ур, то открывается 2-ой
    if second_lvl:
        s_lvl = font.render('Уровень 2', 1, pygame.Color('white'))
        s_lvl_rect = s_lvl.get_rect()
        s_lvl_rect.x = width // 2 - s_lvl.get_width() // 2
        s_lvl_rect.top = height // 2 - s_lvl.get_height() // 2
        screen.blit(s_lvl, s_lvl_rect)

    # Если игрок прошёл 2 ур, то открывается 3-ий
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
            # Проверки на то, нажал ли игрок кнопку
            if event.type == pygame.MOUSEBUTTONDOWN and f_lvl_rect.colliderect(pygame.Rect(*event.pos, 10, 10)):
                current_lvl = first_level
                first_level()
            if event.type == pygame.MOUSEBUTTONDOWN and exit_btn_rect.colliderect(pygame.Rect(*event.pos, 10, 10)):
                pygame.quit()
                sys.exit()
            if (second_lvl and event.type == pygame.MOUSEBUTTONDOWN
                    and s_lvl_rect.colliderect(pygame.Rect(*event.pos, 10, 10))):
                current_lvl = second_level
                second_level()
            if (third_lvl and event.type == pygame.MOUSEBUTTONDOWN
                    and th_lvl_rect.colliderect(pygame.Rect(*event.pos, 10, 10))):
                current_lvl = the_third_level
                the_third_level()
        pygame.display.flip()


def death_screen():
    # Создание кнопок Продолжить и Главное меню
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
            # Проверка на то, нажал ли игрок кнопку
            if event.type == pygame.MOUSEBUTTONDOWN and continue_btn_rect.colliderect(pygame.Rect(*event.pos, 10, 10)):
                current_lvl()
            if event.type == pygame.MOUSEBUTTONDOWN and main_menu_btn_rect.colliderect(pygame.Rect(*event.pos, 10, 10)):
                main_menu()
        pygame.display.flip()


def victory_screen():
    # Создание кнопки Главное меню
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
            # Если кнопку нажали, то запускаем главное меню
            if event.type == pygame.MOUSEBUTTONDOWN and main_menu_btn_rect.colliderect(pygame.Rect(*event.pos, 10, 10)):
                main_menu()
        pygame.display.flip()


def load_image(name, colorkey=None):
    #функция для удобства загрузки фотографий
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
    hp = HealthPoints(all_sprites, spaceship)
    running = True
    meteor = Meteorites(all_sprites)
    all_meteorites.add(meteor)
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


class Boss(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.hp = 20  # Увеличенное количество здоровья для босса
        self.max_hp = 20
        self.image = load_image("boss.png", colorkey=(255, 255, 255))
        self.image = pygame.transform.scale(self.image, (120, 100))  # Измените размер для лучшей видимости
        self.rect = self.image.get_rect(center=(width - 35, height // 2))# Разместить босса в центре верхней части экрана
        self.bullet_interval = 5  # Интервал выпуска патронов
        self.current_time = time.time()  # Текущее время для отслеживания
        self.last_bullet_time = time.time()  # Время последнего выпуска патронов
        self.spawn_interval = 2  # Интервал для создания кораблей противника
        self.last_spawn_time = time.time()  # Время последнего создания
        self.create_opponent_ships()
        self.speed = 2


        if self.last_spawn_time >= self.spawn_interval:
            self.create_opponent_ships()  # Создать корабли противника
            self.last_spawn_time = self.current_time
            self.direction = -1

    def update(self):
        # Двигаем спрайт вверх или вниз
        self.rect.y += self.speed * self.direction

        # Устанавливаем ограничение на движение
        if self.rect.top <= 0:  # Если космический корабль достиг верхнего края экрана
            self.direction = 1  # Изменяем направление вниз
        elif self.rect.bottom >= height:  # Если космический корабль достиг нижнего края экрана
            self.direction = -1


        # Ограничиваем движение корабля экраном
        self.rect.top = max(0, self.rect.top)  # Ограничиваем сверху
        self.rect.bottom = min(height, self.rect.bottom)  # Ограничиваем снизу
        current_time = time.time()
        if current_time - self.last_bullet_time >= self.bullet_interval:
            self.shoot_meteorite()  # Вызываем метод стрельбы метеоритом
            self.last_bullet_time = current_time

        if self.hp <= 0:
            self.kill()

    def create_opponent_ships(self):
        # Создание кораблей противника слева и справа от босса
        for side in [-60, width + 60]:  # На каких координатах будут корабли
            opponent = Opponent(all_sprites)
            opponent.rect.center = (side, random.randint(0, height))  # Размещаем их случайно по высоте
            all_opponents.add(opponent)

    def shoot_meteorite(self):
        # Создаем новый метеорит и помещаем его в группу спрайтов
        meteorite = Meteorites_2(all_sprites)
        meteorite.rect.center = (self.rect.centerx - 15, self.rect.centery)  # Позиция метеорита
        all_meteorites_2.add(meteorite)


class Opponent(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.hp = 3
        self.max_hp = 3
        self.image = load_image("opponent.png", colorkey=(255, 255, 255))
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.speed = 2
        self.reset_pos()
        self.bullet_interval = 1.25
        self.current_time = time.time()
        self.last_bullet_time = time.time()
        all_opponents.add(self)
        self.hp_sprite = HealthPoints(all_sprites, self)

    def reset_pos(self):
        self.rect.y = random.randint(0, height - self.rect.height)
        self.rect.x = width + random.randint(0, 65)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.reset_pos()
        self.current_time = time.time()
        if self.current_time - self.last_bullet_time >= self.bullet_interval:
            bullet = Bullets(all_sprites, self, self.rect.x, self.rect.y)
            self.last_bullet_time = time.time()
        if self.hp <= 0:
            self.hp_sprite.kill()
            self.kill()


opponent_interval = 9


def second_level():
    restart_game()
    spaceship = Spaceship(all_sprites)
    spaceships.add(spaceship)
    hp = HealthPoints(all_sprites, spaceship)
    running = True
    game_time = 60
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('arial', 40)
    opponent = Opponent(all_sprites)
    last_opponent_time = time.time()
    last_bullet_time = 0
    bullet_interval = 0.50

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.USEREVENT:
                game_time -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet_time = time.time()
                if bullet_time - last_bullet_time >= bullet_interval:
                    bullet = Bullets(all_sprites, spaceship, spaceship.rect.x, spaceship.rect.y + 25)
                    last_bullet_time = bullet_time

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

        current_time = time.time()
        if current_time - last_opponent_time >= opponent_interval:
            num_opponents = random.randint(1, 2)
            for _ in range(num_opponents):
                opponent = Opponent(all_sprites)  # создание происходит здесь
                opponent.rect.y = random.randint(0, height - opponent.rect.height)
                opponent.rect.x = width + random.randint(0, width // 2)
            last_opponent_time = current_time

        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(70)


def the_third_level():
    restart_game()
    spaceship = Spaceship(all_sprites)
    spaceships.add(spaceship)
    boss = Boss(all_sprites)  # Босс
    all_sprites.add(boss)
    all_opponents.add(boss)
    hp = HealthPoints(all_sprites, spaceship)
    boss_hp = HealthPoints(all_sprites, boss)
    running = True
    font = pygame.font.SysFont('arial', 30)
    last_bullet_time = 0
    bullet_interval = 0.50

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet_time = time.time()
                if bullet_time - last_bullet_time >= bullet_interval:
                    bullet = Bullets(all_sprites, spaceship, spaceship.rect.x, spaceship.rect.y + 25)
                    last_bullet_time = bullet_time

        if boss.hp <= 0:
            with open('levels') as f:
                data = list(f.read())
                data[2] = '1'
            with open('levels', 'w') as f:
                f.write(''.join(data))
            time.sleep(0.5)
            titles()

        # Отображаем фон
        screen.blit(background, (0, 0))
        text = font.render('Победи босса!', True, pygame.Color('red'))
        screen.blit(text, (width // 2 - text.get_width() // 2, text.get_height() // 2))
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(70)


def restart_game():
    # При запуске уровню очищаем все группы спрайтов
    all_sprites.empty()
    all_opponents.empty()
    spaceships.empty()
    all_meteorites.empty()
    all_meteorites_2.empty()


class Meteorites_2(pygame.sprite.Sprite):
    #создаем второй тип метеорита для босса
    image = load_image("meteor.png", -1) # Указываем colorkey
    image = pygame.transform.scale(image, (40, 40))

    def __init__(self, group):
        super().__init__(group)
        self.image = Meteorites_2.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.speed = 2
        self.dead = True
        self.boom_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x -= self.speed  # Движение справа на лево


class Meteorites(pygame.sprite.Sprite):
    image = load_image("meteor.png", -1) # Указываем colorkey
    image = pygame.transform.scale(image, (50, 50))

    def __init__(self, group):
        super().__init__(group)
        self.image = Meteorites.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.speed = 2
        self.dead = True
        self.boom_time = pygame.time.get_ticks()
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
    hp = 100

    def __init__(self, group):
        super().__init__(group)
        self.max_hp = Spaceship.hp
        self.image = Spaceship.spaceship_image
        self.imageb = Spaceship.image_boom
        self.imageb = pygame.transform.scale(Spaceship.image_boom, (120, 120))
        self.image = pygame.transform.scale(Spaceship.spaceship_image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed = 3
        self.hp = Spaceship.hp
        self.dead = False
        self.boom_time = 0

    def update(self, *args):
        if self.hp <= 0 and not self.dead:
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

        if pygame.sprite.spritecollideany(self, all_meteorites):
            meteor = pygame.sprite.spritecollideany(self, all_meteorites)
            if pygame.sprite.collide_rect_ratio(0.7)(self, meteor):
                self.hp -= 50
                meteor.kill()
        if pygame.sprite.spritecollide(self, all_meteorites_2, True):
            self.hp -= 20


class HealthPoints(pygame.sprite.Sprite):
    # Загрузка картинок
    full_hp_image = load_image('full_hp.png', -1)
    full_hp_image = pygame.transform.scale(full_hp_image, (50, 50))
    half_hp_image = load_image('half_hp.png')
    half_hp_image = pygame.transform.scale(half_hp_image, (50, 50))
    third_hp_image = load_image('1-third_hp.png', -1)
    third_hp_image = pygame.transform.scale(third_hp_image, (50, 50))
    zero_hp_image = load_image('zero_hp.png', -1)
    zero_hp_image = pygame.transform.scale(zero_hp_image, (50, 50))

    def __init__(self, group, owner):
        super().__init__(group)
        self.image = HealthPoints.full_hp_image
        self.rect = self.image.get_rect()
        self.owner = owner
        if isinstance(owner, Spaceship):
            # Если владелец - корабль игрока, то сердечко спавнится в левом верхнем углу
            self.font = pygame.font.SysFont('arial', 30)
            self.rect.x = self.image.get_width() // 4
            self.rect.y = self.image.get_height() // 4
            self.hp_x = self.rect.x + 60
            self.hp_y = self.rect.y + 15
        if isinstance(owner, Opponent):
            # Если владелец - корабль врага, то хп спавнится над ним
            self.font = pygame.font.SysFont('arial', 20)
            self.rect.x = owner.rect.x
            self.rect.y = owner.rect.y - 10
        if isinstance(owner, Boss):
            self.font = pygame.font.SysFont('arial', 30)
            self.hp_x, self.hp_y = width - width // 20, height // 20
            self.rect.x, self.rect.y = self.hp_x - 75, self.hp_y - 10

    def update(self):
        if isinstance(self.owner, Opponent):
            # Если корабль врага, то координаты меняются на его, чтоб хп всегда было над противником
            self.hp_x, self.hp_y = self.owner.rect.x, self.owner.rect.y
        hp = self.font.render(f'{self.owner.hp}', True, pygame.Color('red'))
        screen.blit(hp, (self.hp_x, self.hp_y))

        # Смена картинок в зависимости от кол-ва хп владельца
        if self.owner.hp <= self.owner.max_hp // 2:
            self.image = HealthPoints.half_hp_image
        if self.owner.hp <= self.owner.max_hp // 3:
            self.image = HealthPoints.third_hp_image
        if self.owner.hp <= 0:
            self.image = HealthPoints.zero_hp_image


class Bullets(pygame.sprite.Sprite):
    # загружаем картинки кораблей
    opponent_bullet_image = load_image('opponents_bullet.png')
    opponent_bullet_image = pygame.transform.scale(opponent_bullet_image, (40, 40))
    players_bullet_image = load_image('players_bullet.png')
    players_bullet_image = pygame.transform.scale(players_bullet_image, (25, 25))
    bullet_owners_class = None

    def __init__(self, group, owner, owners_x, owners_y):
        super().__init__(group)
        self.owner = owner
        self.speed = 4
        self.image = None
        if isinstance(owner, Spaceship):
            # если владелец пули - корабль игрока, то устанавливается соответственная картинка
            self.image = Bullets.players_bullet_image
            self.bullet_owners_class = Spaceship
        if isinstance(owner, Opponent):
            # если владелец пули - корабль противника, то устанавливается соответственная картинка
            self.image = Bullets.opponent_bullet_image
            self.bullet_owners_class = Opponent
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = owners_x, owners_y


    def update(self):
        # если владелец пули - корабль игрока, то пули будут лететь в лево, а также при столкновении снимать 1хп врагам
        if self.bullet_owners_class == Spaceship:
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, all_opponents):
                enemy = pygame.sprite.spritecollideany(self, all_opponents)
                if pygame.sprite.collide_rect_ratio(0.62)(self, enemy):
                    enemy.hp -= 1
                    self.kill()

        # если владелец пули - корабль противника, то пули будут лететь вправо и снимать кораблю игрока 10 хп
        if self.bullet_owners_class == Opponent:
            self.rect.x -= self.speed
            if pygame.sprite.spritecollideany(self, spaceships):
                ship = pygame.sprite.spritecollideany(self, spaceships)
                if pygame.sprite.collide_rect_ratio(0.62)(self, ship):
                    ship.hp -= 10
                    self.kill()

        # Проверка на то, что пуля вышла за пределы экрана. если да, то она пропадает
        if self.rect.x > width or self.rect.x < 0:
            self.kill()


def titles():
    screen.fill((0, 0, 0))
    pygame.time.set_timer(pygame.USEREVENT, 950)
    titles_text = ['Поздравляем!', 'Вы прошли игру.', 'Надеемся, что вам понравилось.',
            'Для выхода в главное меню нажмите escape.']
    font = pygame.font.SysFont('arial', 30)
    index = 0
    authors_index = 0
    running = True
    authors_flag = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
            if event.type == pygame.USEREVENT:
                # Если сработал таймер и прошло 950 млс, то выводится текст титров(по одной строчке)
                text = font.render(titles_text[index], 1, pygame.Color('white'))
                text_rect = text.get_rect()
                text_rect.x = width // 2 - text.get_width() // 2
                text_rect.y = text.get_height() // 2 + 50 * index
                index += 1
                if index == len(titles_text):
                    authors_flag = True
                # Если вывелись благодарности, то затем выводятся и авторы
                if authors_flag:
                    authors_list = ['Авторы:', 'Мила', 'Коля', 'Радик']
                    authors = font.render(authors_list[authors_index], 1, pygame.Color('white'))
                    authors_rect = authors.get_rect()
                    authors_rect.x = (width // 2 - authors.get_width() // 2)
                    authors_rect.y = (height // 2) + 35 * authors_index
                    authors_index += 1
                    authors_index = authors_index % len(authors_list)
                    screen.blit(authors, authors_rect)
                index = index % len(titles_text)
                screen.blit(text, text_rect)

        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
