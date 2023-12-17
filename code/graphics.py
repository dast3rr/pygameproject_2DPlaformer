import pygame
import os
import sys
from screeninfo import get_monitors

cube = pygame.sprite.Group()
platforms = pygame.sprite.Group()

monitor = get_monitors()[0]
size = monitor.width, monitor.height

screen = pygame.display.set_mode(size)
fps = 60

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        pass
        image = image.convert_alpha()
    return image


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, a, x, y):
        super().__init__(cube)
        self.a = a
        self.image = pygame.Surface((a, a),
                                    pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, a, a)
        pygame.draw.rect(screen, 'blue', (x, y, a, a))
        self.v = 50

    def update(self):
        if not pygame.sprite.spritecollideany(self, platforms):
            self.rect.y += self.v / fps
        pygame.draw.rect(screen, 'blue', (self.rect.x, self.rect.y, self.a, self.a))


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b):
        w, h = screen.get_size()
        super().__init__(platforms)
        self.small_image = False
        self.cords = (w // 3 + x * 2, h // 6 + y * 2, a * 2, b * 2)
        self.image = pygame.Surface((a, b),
                                    pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(w // 3 + x * 2, h // 3 + y * 2, a * 2, b * 2)
        pygame.draw.rect(screen, 'black', self.rect)

    def update(self):
        pygame.draw.rect(screen, 'black', self.cords)
