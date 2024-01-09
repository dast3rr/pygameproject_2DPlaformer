import pygame
from graphics import screen


class Base(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(volume_controller)
        self.image = pygame.Surface((500, 30), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(100, 100, self.image.get_width(), self.image.get_height())
        pygame.draw.rect(self.image, (150, 150, 150), self.image.get_rect(), border_radius=10)


class Slider(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(volume_controller)
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(100 + 5 * pygame.mixer.music.get_volume() * 100, 100,
                                self.image.get_width(), self.image.get_height())
        pygame.draw.circle(self.image, (0, 0, 0), (15, 15), 15)

        self.mouse_x_on_slider = 0
        self.moving = False

    def update(self, *args):
        if args:
            event = args[0]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.moving = True
                    self.mouse_x_on_slider = event.pos[0] - self.rect.x
            if event.type == pygame.MOUSEBUTTONUP:
                self.moving = False
            if event.type == pygame.MOUSEMOTION:
                if self.moving:
                    if 85 <= event.pos[0] - self.mouse_x_on_slider <= 585:
                        self.rect.x = event.pos[0] - self.mouse_x_on_slider
                        pygame.mixer.music.set_volume((self.rect.x - 100) / 5 / 100)


class Filler(pygame.sprite.Sprite):
    def __init__(self, slider):
        super().__init__(volume_controller)
        self.image = pygame.Surface((500, 30), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(100, 100, slider.rect.x - 100, self.image.get_height())
        pygame.draw.rect(self.image, (255, 255, 255), self.rect, border_radius=10)

    def update(self, slider):
        self.rect.width = slider.rect.x - 100
        pygame.draw.rect(self.image, (255, 255, 255), self.rect, border_radius=10)

    def draw(self):
        pygame.draw.rect(self.image, (255, 255, 255), self.rect, border_radius=10)

volume_controller = pygame.sprite.Group()