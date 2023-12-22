from graphics import Platform, platforms, screen, fps, size, MainCharacter, vertical_platforms, horizontal_platforms, \
    character
from data import cords

import pygame
import os

def initialization():
    for cord in cords:
        x, y, a, b = cord
        Platform(x + 1, y, a - 2, b, platforms, horizontal_platforms)
        Platform(x, y + 1, a, b - 2, platforms, vertical_platforms)

    # главный герой
    main_character = MainCharacter(0, 0, 20, 40)
    return main_character


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.x = size[0] // 2
        self.y = size[1] // 2

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.x
        obj.rect.y += self.y

    # позиционировать камеру на объекте target
    def update(self, target):
        d_x = main_character.rect.x - self.x
        d_y = main_character.rect.y - self.y
        if d_x > 50:
            for platform in platforms:
                platform.rect.x -= d_x - 50
                self.x -= d_x - 50
        elif d_x < -50:
            for platform in platforms:
                platform.rect.x -= d_x + 50
                self.x -= d_x + 50
        if d_y > 50:
            for platform in platforms:
                platform.rect.y -= d_y - 50
                self.y -= d_y - 50
        elif d_y < -50:
            for platform in platforms:
                platform.rect.y -= d_y + 50
                self.y -= d_y + 50


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
    start_jump_altitude = -100000
    start_jump_from_wall_position = 0
    jump = False
    jump_from_wall = False
    speeds_before_jump = [0, 0]

    # инициализация главного героя и платформ.
    main_character = initialization()

    # перемещение в стороны
    right = left = 0

    camera = Camera()
    running = True
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

                # если нажат shift то ускоряется
                if keys[pygame.K_LSHIFT]:
                    move_speed = 120
                else:
                    move_speed = 80

                # при нажатии на пробел - прыжок
                if event.key == pygame.K_SPACE and (main_character.get_hor() or main_character.get_ver()):
                    start_jump_altitude = main_character.rect.y + 1
                    main_character.rect.y -= 2
                    if main_character.get_ver() and main_character.get_hor():
                        main_character.rect.x += 1
                        if main_character.get_ver():
                            main_character.rect.x -= 2
                    jump = True
                    if main_character.get_ver():
                        jump_from_wall = True
                        speeds_before_jump = [0, 0]
                        main_character.rect.x -= 1
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
                if event.key == pygame.K_LSHIFT:
                    move_speed = 80

        # цвет можно поменять. Это будет цвет фона
        screen.fill(pygame.color.Color(200, 200, 200))

        # перемещение в стороны
        move_hor = right + left

        if move_hor < 0:
            # если движение влево, то изначально значение отрицательно
            r = range(-(move_hor * move_speed) // fps)
        else:
            r = range((move_hor * move_speed) // fps)
        for i in r:
            # начально условие
            condition = main_character.get_ver()
            # потом двигаю персонажа
            main_character.rect.x += move_hor
            # если условие не поменялось, то возвращаю обратно, и в любом случаю прекращаю движение
            if main_character.get_ver():
                if condition:
                    main_character.rect.x -= move_hor
                jump = False
                break

        if main_character.get_ver() and not jump:
            fall_speed = 60
        elif not jump:
            fall_speed = 120
        if jump:
            # при прыжке, на самой верхней точке скорость меньше
            fall_speed = -(60 - start_jump_altitude + main_character.rect.y) * 5
            if not fall_speed:
                jump = False
                fall_speed = 120

        if jump_from_wall:
            if abs(main_character.rect.x - start_jump_from_wall_position) > 20:
                jump_from_wall = False
                right, left = speeds_before_jump
                speeds_before_jump = [0, 0]

        if fall_speed:
            # падение и скольжение
            if fall_speed < 0:
                # отрицательно при прыжке
                r = range(-(fall_speed // fps))
            else:
                r = range(fall_speed // fps)
            for i in r:
                condition = main_character.get_hor()
                main_character.rect.y += fall_speed // abs(fall_speed)
                if main_character.get_ver():
                    if jump:
                        main_character.rect.y += 3
                        jump = False
                        break
                    if condition:
                        main_character.rect.y -= fall_speed // abs(fall_speed)
                    break

        camera.update(main_character)

        # отрисовываю все группы спрайтов
        platforms.draw(screen)
        platforms.update()

        character.draw(screen)
        character.update()

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
