from graphics import Platform, platforms, screen, fps, size, MainCharacterForVertical, MainCharacterForHorizontal, character
from data import cords

import pygame
import os


if __name__ == '__main__':
    # Перемещаю экран на центр
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.display.set_mode(size)
    # таймер для обновления фпс - 60
    clock = pygame.time.Clock()

    # скорость падения, прыжка и передвижения
    move_speed = 80
    fall_speed = 120
    jump_speed = 120

    # пустое значение
    start_jump_altitude = 0
    jump = False

    # Создаю чёрные прямоугольники стен по кординатам из data.py
    for cord in cords:
        Platform(*cord)

    # создаю два прямоугольника, один отвечает за пересечение по вертикали, другой - по горизонтали
    main_hor = MainCharacterForHorizontal(100, 185, 20, 40)
    main_ver = MainCharacterForVertical(100, 185, 40, 20)

    # перемещение в стороны
    right = left = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # если нажаты клавиши
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    right = 1
                elif event.key == pygame.K_a:
                    left = -1

                # если нажат shift то ускоряется
                elif event.mod & pygame.K_LSHIFT:
                    move_speed = 120

                # при нажатии на пробел - прыжок
                elif event.key == pygame.K_SPACE and not jump:
                    start_jump_altitude = main_hor.rect.y
                    jump = True

            # если отпускается какая-либо клавиша
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = 0
                elif event.key == pygame.K_a:
                    left = 0

                elif event.key == pygame.K_LSHIFT:
                    move_speed = 80

        # цвет можно поменять. Это будет цвет фона
        screen.fill(pygame.color.Color(200, 200, 200))
        # перемещение в стороны. Если нажаты клавиши, то соответствующие значения
        move_hor = right + left

        # двигаю
        main_hor.rect.x += (move_hor * move_speed) / fps
        main_ver.rect.x += (move_hor * move_speed) / fps

        # проверяю пересечение с блоками
        condition_ver = main_ver.get_condition()
        condition_hor = main_hor.get_condition()

        # если пересекается, то возвращаю обратно
        if condition_ver:
            main_hor.rect.x -= (move_hor * move_speed) / fps
            main_ver.rect.x -= (move_hor * move_speed) / fps

        # падать или нет
        if condition_hor or jump:
            fall_speed = 0
        elif not condition_hor and not condition_ver:
            fall_speed = 120

        # перемещение по высоте
        main_hor.rect.y += fall_speed / fps
        main_ver.rect.y += fall_speed / fps

        # если прыжок, то двигаться вверх
        if jump:
            main_hor.rect.y -= jump_speed / fps
            main_ver.rect.y -= jump_speed / fps

        # если улетели далеко от начальной точки прыжка или же встертили стену, то прыжок заверщается
        if main_hor.rect.y - start_jump_altitude == -70:
            jump = False

        # если врезались
        if main_hor.get_condition():
            if not jump:
                main_hor.rect.y -= fall_speed / fps
                main_ver.rect.y -= fall_speed / fps
            else:
                fall_speed = 120
                main_hor.rect.y += fall_speed / fps
                main_ver.rect.y += fall_speed / fps
                jump = False

        # отрисовываю все группы спрайтов
        platforms.draw(screen)
        platforms.update()

        character.draw(screen)
        character.update()

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
