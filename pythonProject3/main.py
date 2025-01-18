import pygame
import sys

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
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отображаем фон
    screen.blit(background, (0, 0))

    # Обновляем экран
    pygame.display.flip()

# Завершение Pygame
pygame.quit()