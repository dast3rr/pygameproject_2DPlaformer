from graphics import platforms, screen, fps, size, \
    character, enemies, main_character, menu
from data import move_speed, start_jump_from_wall_position, start_jump_altitude, jump, jump_from_wall, \
    jump_speed, fall_speed
from menu import InGameMenu

import pygame
import os


# класс камеры
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.x = size[0] // 2
        self.y = size[1] // 2

    # позиционировать камеру на объекте target
    def update(self):
        global start_jump_altitude, start_jump_from_wall_position
        d_x = main_character.rect.x - self.x
        d_y = main_character.rect.y - self.y

        r = 30 * N
        k = 0
        if d_x > r:
            k = -1
        elif d_x < -r:
            k = 1
        if k:
            main_character.rect.x -= d_x + r * k
            self.x = main_character.rect.x + r * k
            start_jump_from_wall_position -= (d_x + r * k)
            for sprite in platforms:
                sprite.rect.x -= (d_x + r * k)
            for sprite in enemies:
                sprite.rect.x -= (d_x + r * k)

        k = 0
        if d_y > r:
            k = -1
        elif d_y < -r:
            k = 1

        if k:
            main_character.rect.y -= d_y + r * k
            self.y = main_character.rect.y + r * k
            start_jump_altitude -= (d_y + r * k)
            for sprite in platforms:
                sprite.rect.y -= (d_y + r * k)
            for sprite in enemies:
                sprite.rect.y -= (d_y + r * k)


if __name__ == '__main__':
    # Перемещаю экран на центр
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    N = 10

    pygame.init()
    pygame.display.set_mode(size)
    # таймер для обновления фпс - 60
    clock = pygame.time.Clock()

    # пустое значение
    start_jump_altitude = -100000
    start_jump_from_wall_position = 0
    jump = False
    jump_from_wall = False
    speeds_before_jump = [0, 0]

    # перемещение в стороны
    right = left = 0

    paused_menu = InGameMenu()

    smooth_surface = pygame.Surface(size)
    smooth_surface.set_alpha(60)

    count_fall = False
    counter_fall = 0


    camera = Camera()
    running = True
    game_paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # если нажаты клавиши
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_d]:
                    if not jump_from_wall:
                        right = 1
                    else:
                        speeds_before_jump[0] = 1
                if keys[pygame.K_a]:
                    if not jump_from_wall:
                        left = -1
                    else:
                        speeds_before_jump[1] = -1
                if keys[pygame.K_h]:
                    main_character.heal()

                if keys[pygame.K_ESCAPE]:
                    if game_paused:
                        game_paused = False
                    else:
                        game_paused = True

                # при нажатии на пробел - прыжок
                if event.key == pygame.K_SPACE and (main_character.get_hor() or main_character.get_ver()):
                    start_jump_altitude = main_character.rect.y + 1
                    # проверка на зацепление за текстуры(был баг без этого)
                    main_character.rect.y -= 2
                    if main_character.get_ver() and main_character.get_hor():
                        main_character.rect.x += 1
                        if main_character.get_ver():
                            main_character.rect.x -= 2
                    # объявляю прыжок
                    jump = True
                    if main_character.get_ver():  # если есть касани вертикально стены, то объявляю прыжок от стены
                        jump_from_wall = True
                        speeds_before_jump = [0, 0]
                        main_character.rect.x -= 1
                        # запоминаю скорости
                        if main_character.get_ver():
                            right = 1
                            left = 0
                        else:
                            right = 0
                            left = -1

                        main_character.rect.x += 1
                        start_jump_from_wall_position = main_character.rect.x
                    else:
                        jump_from_wall = False

            # если отпускается какая-либо клавиша
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = 0
                if event.key == pygame.K_a:
                    left = 0

        # цвет можно поменять. Это будет цвет фона
        screen.fill(pygame.color.Color(200, 200, 200))

        # перемещение в стороны
        move_hor = right + left
        if main_character.get_hor() or main_character.get_ver():
            count_fall = False

        if not main_character.get_hor() and not jump and not count_fall:
            count_fall = True
            counter_fall = 0

        # определение скорости падения
        if main_character.get_ver() and not jump:
            fall_speed = 15 * N + counter_fall
        elif not jump:
            fall_speed = 45 * N + counter_fall
        if jump:
            # при прыжке, на самой верхней точке скорость меньше
            fall_speed = -(25 * N - start_jump_altitude + main_character.rect.y) * 7
            if fall_speed > -20:
                counter_fall = 0
                count_fall = True
                jump = False
                fall_speed = 45 * N
        # если совершается прыжок от стены
        if jump_from_wall:
            # если уже далеко от стены
            if abs(main_character.rect.x - start_jump_from_wall_position) > 2 * N:
                jump_from_wall = False
                right, left = speeds_before_jump
                speeds_before_jump = [0, 0]


        camera.update()

        # отрисовываю все группы спрайтов
        platforms.draw(screen)
        platforms.update()

        character.draw(screen)

        if game_paused:
            screen.blit(smooth_surface, (0, 0))
            menu.draw(screen)
            InGameMenu.draw_menu_buttons(paused_menu)
            if paused_menu.resume_button.get_pressed():
                game_paused = False
        else:
            jump = main_character.update(move_hor, jump, move_speed, fall_speed)
            enemies.update()

        if count_fall:
            counter_fall += 6

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
