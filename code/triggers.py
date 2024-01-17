from graphics import Platform, platforms, vertical_platforms,  trigger_blocks, character, screen, load_image, enemies, Vengefly
from data import global_cords, N, respawn_cords
import pygame


class Boss_Wall_Lock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(trigger_blocks)
        self.rect = pygame.rect.Rect(1050 * N, 900 * N, 100 * N, 200 * N)
        self.lock_wall = False
        self.boss = None

    def update(self):
        if pygame.sprite.spritecollideany(self, character) and not self.lock_wall:
            self.lock_wall = True
            x, y, a, b = -40, -100, 10, 200
            Platform(x, y, a, b, platforms, vertical_platforms)
            platforms.draw(screen)

            mouthwing_graphics = []
            mouthwing_images = [(load_image('mouthwing\\mouthwing_flying.png'), 4),
                                (load_image('mouthwing\\mouthwing_turning.png'), 2),
                                (load_image('mouthwing\\mouthwing_diying.png'), 2)]

            for image, row in mouthwing_images:
                k = 400 / image.get_height()
                scaled_image = pygame.transform.scale(image, (
                    image.get_width() * k, image.get_height() * k))
                mouthwing_graphics.append((scaled_image, row, 1))

            mouthwing = Vengefly(70, -30, mouthwing_graphics, enemies)
            mouthwing.rect.h = 400
            mouthwing.rect.w = 500
            mouthwing.agr_radius = 1000
            mouthwing.hp = 20
            mouthwing.dropping_money = 100
            mouthwing.speed = 1
            self.boss = mouthwing
#         if self.boss.hp == 0:
#             MindSphere()
#
#
# class MindSphere(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__(trigger_blocks)
#         self.rect = pygame.rect.Rect(1050 * N, 900 * N, 100 * N, 200 * N)


