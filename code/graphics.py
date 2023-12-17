import pygame
import os
import sys

cube = pygame.sprite.Group()
platforms = pygame.sprite.Group()
size = width, height = 500, 500
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
    def __init__(self, a, b, x, y):
        super().__init__(platforms)
        self.cords = (x, y, a, b)
        self.image = pygame.Surface((a, b),
                                    pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, a, b)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, a, b))

    def update(self):
        pygame.draw.rect(screen, (100, 100, 100), self.cords)