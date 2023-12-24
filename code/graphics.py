import pygame
import os
import sys
from screeninfo import get_monitors








# def load_image(name, colorkey=None):
#     fullname = os.path.join('data', name)
#     if not os.path.isfile(fullname):
#         print(f"Файл с изображением '{fullname}' не найден")
#         sys.exit()
#     image = pygame.image.load(fullname)
#
#     if colorkey is not None:
#         image = image.convert()
#         if colorkey == -1:
#             colorkey = image.get_at((0, 0))
#         image.set_colorkey(colorkey)
#     else:
#         image = image.convert_alpha()
#     return image

# класс для горизонтальных пересечений и картинки
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b, color, *groups):
        # всякие кординаты
        self.color = color
        super().__init__(character, *groups)
        w, h = screen.get_size()
        self.a, self.b = a * N, b * N
        x *= N
        y *= N

        self.image = pygame.Surface([self.a, self.b])
        self.image.fill(color)
        self.cords = (w // 2 + x, h // 2 + y, self.a, self.b)
        self.rect = pygame.Rect(w // 2 + x - 1, h // 2 + y - 1, self.a + 2, self.b + 2)
        pygame.draw.rect(screen, self.color, self.rect)

    def get_hor(self):
        return pygame.sprite.spritecollideany(self, horizontal_platforms)

    def get_ver(self):
        return pygame.sprite.spritecollideany(self, vertical_platforms)


class MainCharacter(Character):
    # рисование
    def update(self, *args):
        move_hor, jump, move_speed, fall_speed = args

        if move_hor < 0:
            # если движение влево, то изначально значение отрицательно
            r = range(-(move_hor * move_speed) // fps)
        else:
            r = range((move_hor * move_speed) // fps)
        for i in r:
            # начально условие
            condition = self.get_ver()
            # потом двигаю персонажа
            self.rect.x += move_hor
            # если условие не поменялось, то возвращаю обратно, и в любом случаю прекращаю движение
            if self.get_ver():
                if condition:
                    self.rect.x -= move_hor
                jump = False
                break

        if fall_speed:
            # падение и скольжение
            if fall_speed < 0:
                # отрицательно при прыжке
                r = range(-(fall_speed // fps))
            else:
                r = range(fall_speed // fps)
            for i in r:
                condition = self.get_hor()
                self.rect.y += fall_speed // abs(fall_speed)
                if self.get_ver():
                    if jump:
                        self.rect.y += 3
                        jump = False
                        break
                    if condition:
                        self.rect.y -= fall_speed // abs(fall_speed)
                    break
        return jump


class Enemy(Character):
    def update(self):
        pass


# класс стен
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b, *groups):
        w, h = screen.get_size()  # ширина и высота окна
        self.a, self.b = a * N, b * N
        x *= N
        y *= N
        super().__init__(*groups)
        # кординаты и картинка. Картинка для последующей обработки столкновений
        self.cords = (w // 2 + x, h // 2 + y, self.a, self.b)
        self.image = pygame.Surface((self.a, self.b),
                                    pygame.SRCALPHA, 32)

        # начальное положение. Чтобы поменять self.rect.x = 100 или self.rect.y = 200
        self.rect = pygame.Rect(w // 2 + x, h // 2 + y, self.a, self.b)
        pygame.draw.rect(screen, 'black', self.rect)

    # обновление положения
    def update(self):
        pygame.draw.rect(screen, 'black', self.rect)

def initialization():
    cords = [(-100, -185, 69, 391), (-100, -185, 191, 68), (-100, 20, 102, 186), (-100, 20, 227, 34),
             (-100, 144, 647, 62),
             (-100, -185, 300, 31), (245, -185, 302, 68), (81, -185, 10, 180), (81, -68, 170, 17), (482, -185, 65, 391),
             (162, 40, 166, 66), (245, -185, 302, 31), (352, 38, 192, 74), (290, -72, 160, 17), (402, -17, 48, 30),
             (110, -115, 50, 20), (180, -130, 30, 10)]
    for cord in cords:
        x, y, a, b = cord
        Platform(x + 1 / N, y, a - 2 / N, b, platforms, horizontal_platforms)
        Platform(x, y + 1 / N, a, b - 2 / N, platforms, vertical_platforms)

    # главный герой
    Enemy(-30, 10, 10, 10, 'red', enemies)
    main_character = MainCharacter(0, 0, 10, 20, 'white')

    return main_character

# получаю параметры монитора, по ним делаю окно игры
monitor = get_monitors()[0]
size = monitor.width, monitor.height

# сам экран
screen = pygame.display.set_mode(size)
# частота обноления экрана
fps = 60

# группы спрайтов
platforms = pygame.sprite.Group()
character = pygame.sprite.Group()
horizontal_platforms = pygame.sprite.Group()
vertical_platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
N = 6
main_character = initialization()




