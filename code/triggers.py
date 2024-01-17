from graphics import main_character, Platform, platforms, vertical_platforms, horizontal_platforms, trigger_blocks, character, screen
from data import global_cords, N, respawn_cords
import pygame


class Boss_Wall_Lock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(trigger_blocks)
        self.rect = pygame.rect.Rect(1050 * N, 900 * N, 100 * N, 200 * N)
        self.lock_wall = False

    def update(self):
        if pygame.sprite.spritecollideany(self, character) and not self.lock_wall:
            self.lock_wall = True
            x, y, a, b = -40, -100, 10, 200
            Platform(x, y, a, b, platforms, vertical_platforms)
            platforms.draw(screen)





