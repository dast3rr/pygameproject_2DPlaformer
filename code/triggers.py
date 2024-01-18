from graphics import Platform, platforms, vertical_platforms, trigger_blocks, character, screen, load_image, enemies, \
    Vengefly, main_character, background_image
from data import global_cords, N, respawn_cords
import pygame
from load_music import battle_music, first_loc_music


class Boss_Wall_Lock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(trigger_blocks)
        self.rect = pygame.rect.Rect(1050 * N, 900 * N, 100 * N, 200 * N)
        self.image = pygame.surface.Surface((self.rect.w, self.rect.y))
        self.image.set_alpha(0)
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
            mouthwing.hp = 1
            mouthwing.dropping_money = 100
            mouthwing.speed = 1
            self.boss = mouthwing
            battle_music()
            pygame.mixer.music.play(-1, fade_ms=50)

        if self.boss is not None:
            if self.boss.hp == 0:
                self.boss.hp = 1
                MindSphere(self.boss.rect.x, self.boss.rect.y - 200)
                first_loc_music()
                pygame.mixer.music.play(-1, fade_ms=50)


class MindSphere(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(trigger_blocks)
        self.rect = pygame.rect.Rect(x, y, 50, 50)
        self.image = load_image('effects\\white_sphere.png')
        self.image = pygame.transform.scale(self.image, (500, 500))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.sprite.collide_mask(self, main_character):
            print(respawn_cords[0], global_cords[0])
            print(respawn_cords[1], global_cords[1])
            main_character.rect.x = 22800 - respawn_cords[0] - global_cords[0] - main_character.rect.x + screen.get_width()
            if not respawn_cords[0]:
                main_character.rect.x -= screen.get_width() // 2
            main_character.rect.y = 23800 - respawn_cords[1] - global_cords[1] - main_character.rect.y + screen.get_height()

            # background_image.image = pygame.transform.scale(load_image('astral_word_background.png'),
            #                                                 (screen.get_width() * 2, screen.get_height()))
