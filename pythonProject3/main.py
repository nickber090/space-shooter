import pygame
import sys


def main_menu():
    fon = pygame.transform.scale(pygame.image.load('intro_fon.jpg'), size)
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

# Инициализация Pygame
pygame.init()

# Установим размеры окна
size = width, height = 900, 400
screen = pygame.display.set_mode(size)

# Зададим заголовок окна
pygame.display.set_caption("Cosmos Background")

# Загрузим изображение
try:
    background = pygame.image.load('cosmos.png')
except pygame.error:
    print("Не удалось загрузить изображение. Проверьте наличие файла cosmos.png.")
    pygame.quit()
    sys.exit()

# Основной игровой цикл
main_menu()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    # Отображаем фон
    screen.blit(background, (0, 0))

    # Обновляем экран
    pygame.display.flip()

# Завершение Pygame
pygame.quit()
