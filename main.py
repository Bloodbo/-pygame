import pygame
import time

# Инициализация Pygame
pygame.init()

# Создание экрана
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('My Game')

# Загрузка иконки
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

# Загрузка фона и анимаций
bg = pygame.image.load('images/1670754026.png')

walk_left = [
    pygame.image.load('images/pes_left/pes_levo1.png'),
    pygame.image.load('images/pes_left/pes_levo2.png'),
    pygame.image.load('images/pes_left/pes_levo3.png'),
    pygame.image.load('images/pes_left/pes_levo4.png'),
]

walk_right = [
    pygame.image.load('images/pes_right/pes_pravo1.png'),
    pygame.image.load('images/pes_right/pes_pravo2.png'),
    pygame.image.load('images/pes_right/pes_pravo3.png'),
    pygame.image.load('images/pes_right/pes_pravo4.png'),
]

# Загрузка спрайта препятствия
obstacle_img = pygame.image.load('images/obstacle.png')
obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))  # Уменьшение размера препятствия

# Список препятствий (координаты x, y)
obstacles = [
    (600, 450),
    (800, 450),
    (1000, 450)
]

# Инициализация переменных игрока
player_x = 300
player_y = 400
player_speed = 1  # Уменьшена скорость движения игрока
is_jumping = False
jump_speed = 10
gravity = 0.5
player_velocity_y = 0
player_direction = 'right'

# Инициализация переменных фона
bg_x = 0

# Инициализация счетчика анимации
player_anim_count = 0

# Управление скоростью анимации
animation_speed = 0.3  # Увеличен интервал между кадрами анимации для замедления
last_update_time = time.time()

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получение состояния клавиш
    keys = pygame.key.get_pressed()

    # Обновление позиции игрока и фона
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        player_direction = 'left'
        bg_x += player_speed  # Движение фона в противоположном направлении

    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        player_direction = 'right'
        bg_x -= player_speed  # Движение фона в противоположном направлении

    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
            player_velocity_y = -jump_speed

    if is_jumping:
        player_y += player_velocity_y
        player_velocity_y += gravity
        if player_y >= 400:  # Проверка земли (y = 400 - это пол)
            player_y = 400
            is_jumping = False
            player_velocity_y = 0

    # Ограничение движений игрока в пределах окна
    if player_x < 0:
        player_x = 0
    if player_x > 800 - walk_right[0].get_width():
        player_x = 800 - walk_right[0].get_width()

    # Анимация игрока
    current_time = time.time()
    if current_time - last_update_time > animation_speed:
        last_update_time = current_time
        player_anim_count += 1
        if player_anim_count >= len(walk_right):
            player_anim_count = 0

    # Отрисовка фона и анимации
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + bg.get_width(), 0))  # Второе изображение фона для бесшовного скроллинга

    if bg_x <= -bg.get_width():
        bg_x = 0  # Сброс фона для бесшовного скроллинга

    # Отрисовка препятствий
    for obstacle_x, obstacle_y in obstacles:
        screen.blit(obstacle_img, (obstacle_x, obstacle_y))

        # Проверка столкновения с препятствием
        if (player_x < obstacle_x + obstacle_img.get_width() and
                player_x + walk_right[0].get_width() > obstacle_x and
                player_y < obstacle_y + obstacle_img.get_height() and
                player_y + walk_right[0].get_height() > obstacle_y):
            if player_direction == 'right':
                player_x = obstacle_x - walk_right[0].get_width()
            else:
                player_x = obstacle_x + obstacle_img.get_width()

    if player_direction == 'right':
        screen.blit(walk_right[player_anim_count], (player_x, player_y))
    else:
        screen.blit(walk_left[player_anim_count], (player_x, player_y))

    # Обновление экрана
    pygame.display.update()

# Завершение Pygame
pygame.quit()
