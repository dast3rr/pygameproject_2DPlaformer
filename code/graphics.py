import pygame
import os
import sys
from screeninfo import get_monitors

CAN_MOVE = True
CAN_FALL = False

# группы спрайтов
platforms = pygame.sprite.Group()
character = pygame.sprite.Group()

# получаю параметры монитора, по ним делаю окно игры
monitor = get_monitors()[0]
size = monitor.width, monitor.height

# сам экран
screen = pygame.display.set_mode(size)
# частота обноления экрана
fps = 60

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
#         pass
#         image = image.convert_alpha()
#     return image

# класс для горизонтальных пересечений и картинки
class MainCharacterForHorizontal(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b):
        # всякие кординаты
        super().__init__(character)
        w, h = screen.get_size()
        self.image = pygame.Surface((a, b),
                                    pygame.SRCALPHA, 32)
        self.cords = (w // 3 + x * 2 + (b - a // 2), h // 6 + y * 2, a, b)
        self.rect = pygame.Rect(w // 3 + x * 2, h // 6 + y * 2, b, b)
        pygame.draw.rect(screen, 'white', self.rect)

    def update(self):
        pygame.draw.rect(screen, 'white', self.rect)

    # есть ли перисечение
    def get_condition(self):
        return pygame.sprite.spritecollideany(self, platforms)

# класс только для вертикальных перемещений
class MainCharacterForVertical(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b):
        super().__init__(character)
        # всякие кординаты
        w, h = screen.get_size()
        self.image = pygame.Surface((a, b),
                                    pygame.SRCALPHA, 32)
        self.cords = (w // 3 + x * 2, h // 6 + y * 2 + (a - b // 2), a, b)
        self.rect = pygame.Rect(w // 3 + x * 2, h // 6 + y * 2, a, a)

    # есть ли пересечение
    def get_condition(self):
        return pygame.sprite.spritecollideany(self, platforms)


# класс стен
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b):
        w, h = screen.get_size()  # ширина и высота окна
        super().__init__(platforms)
        # кординаты и картинка. Картинка для последующей обработки столкновений
        self.cords = (w // 3 + x * 2, h // 6 + y * 2, a * 2, b * 2)
        self.image = pygame.Surface((a, b),
                                    pygame.SRCALPHA, 32)

        # начальное положение. Чтобы поменять self.rect.x = 100 или self.rect.y = 200
        self.rect = pygame.Rect(w // 3 + x * 2, h // 6 + y * 2, a * 2, b * 2)
        pygame.draw.rect(screen, 'black', self.rect)

    # обновление положения
    def update(self):
        pygame.draw.rect(screen, 'black', self.cords)
