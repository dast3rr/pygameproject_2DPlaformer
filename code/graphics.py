import pygame
import os
import sys
from screeninfo import get_monitors
from data import global_x, global_y


def load_image(name, colorkey=None):
    fullname = os.path.join('..\data', name)
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
        image = image.convert_alpha()
    return image


# класс для горизонтальных пересечений и картинки
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, graphics, *groups):
        # всякие кординаты
        super().__init__(character, *groups)
        w, h = screen.get_size()
        x *= N
        y *= N

        self.frames = []
        # графика
        for i in range(len(graphics)):
            sheet, columns, rows = graphics[i]
            self.cut_sheet(sheet, columns, rows, x, y)

        self.cur_frame = 0
        self.cur_sheet = 0
        self.image = self.frames[self.cur_sheet][self.cur_frame]
        self.rect = pygame.rect.Rect(x, y, 78, 130)
        self.rect = self.rect.move(x + w // 2 + 20, y + h // 2)
        self.count_flip = 0

    # создание анимации
    def cut_sheet(self, sheet, columns, rows, x, y):
        res = []
        if len(self.frames) == 1 and type(self) == Knight:
            count = 2
        elif len(self.frames) == 1 and type(self) == Crawlid:
            count = 4
        else:
            count = 1

        self.rect = pygame.Rect(x, y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        if type(self) == Knight:
            if len(self.frames) == 4:
                z = 1.6
            else:
                z = 1
            x = 1
        else:
            z = 0
            x = 0
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i + 20 * x, self.rect.h * j)
                image = sheet.subsurface(pygame.Rect(
                    frame_location, (self.rect.w - 40 * z, self.rect.h)))
                for _ in range(count):
                    res.append(image)

        self.frames.append(res)

    def get_hor(self):
        return pygame.sprite.spritecollideany(self, horizontal_platforms)

    def get_ver(self):
        return pygame.sprite.spritecollideany(self, vertical_platforms)


class Knight(Character):
    def __init__(self, x, y, graphics, *groups):
        super().__init__(x, y, graphics, *groups)
        self.health = 5
        self.healings = 6
        self.money = 0
        heart_image = load_image('heart.png')
        heal_image = load_image('heal.png')
        money_image = load_image('money.png')
        self.heart_image = pygame.transform.scale(heart_image, (100, 60))
        self.heal_image = pygame.transform.scale(heal_image, (60, 60))
        self.money_image = pygame.transform.scale(money_image, (60, 60))
        self.non_damage_count = 0
        self.damage = False
        self.old_move_hor = 0

        self.attack_radius = 40
        self.attack_damage = 1
        self.can_damage = False
        self.view_direcion = 0

        self.resist = False
        self.resist_count = 0


    # рисование
    def update(self, *args):
        move_hor, jump, move_speed, fall_speed = args
        if move_hor:
            self.view_direcion = move_hor // abs(move_hor)

        if move_hor < 0:
            # если движение влево, то изначально значение отрицательно
            r = range(-(move_hor * move_speed) // fps)
        else:
            r = range((move_hor * move_speed) // fps)
        for _ in r:
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
            for _ in r:
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

        self.update_healthbar()
        self.update_heals()
        self.update_money()
        self.update_damage_resistant()

        if self.count_flip == 3:
            self.count_flip = 0
            if move_hor == 0 and self.cur_sheet == 0:
                self.cur_frame = 0
            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.cur_sheet])
            self.image = self.frames[self.cur_sheet][self.cur_frame]
            if move_hor == -1 or self.old_move_hor == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            self.mask = pygame.mask.from_surface(self.image)

        self.count_flip += 1
        if move_hor:
            self.old_move_hor = move_hor

        return jump

    def update_healthbar(self):
        for i in range(self.health):
            x = 50 + i * 30
            y = 20
            screen.blit(self.heart_image, (x, y))
        if self.damage:
            self.non_damage_count += 2 / fps
        if self.non_damage_count > 2:
            self.damage = False
            self.non_damage_count = 0

    def heal(self):
        if self.healings > 0 and self.health < 5:
            self.health += 1
            self.healings -= 1

    def update_heals(self):
        screen.blit(self.heal_image, (60, 80))
        font = pygame.font.Font(None, 60)
        text = font.render(str(self.healings), True, pygame.Color('White'))
        screen.blit(text, (130, 80))

    def add_money(self, amount):
        self.money += amount

    def update_money(self):
        screen.blit(self.money_image, (60, 140))
        font = pygame.font.Font(None, 60)
        text = font.render(str(self.money), True, pygame.Color('White'))
        screen.blit(text, (130, 140))

    def attacking(self):
        if self.view_direcion == 1:
            attacking_rect = pygame.Rect(self.rect.topright[0], self.rect.y, self.attack_radius, self.rect.width)
        elif self.view_direcion == -1:
            attacking_rect = pygame.Rect(self.rect.x - self.attack_radius, self.rect.y,
                                         self.attack_radius, self.rect.height)

        for sprite in enemies:
            if attacking_rect.colliderect(sprite.rect):
                sprite.get_damage(self.attack_damage)
                pygame.draw.rect(sprite.image, pygame.Color('Blue'), sprite.rect)

    def get_damage(self, damage):
        if not self.resist:
            self.health -= damage
            self.resist = True

    def update_damage_resistant(self):
        if self.resist:
            self.resist_count += 1
        if self.resist_count == 90:
            self.resist = False
            self.resist_count = 0



class Enemy(Character):
    def __init__(self, x, y, graphics, *groups):
        super().__init__(x, y, graphics, *groups)
        self.hp = 3
        self.dropping_money = 10
        self.reverse_count = 0

    def get_damage(self, damage):
        self.hp -= damage

    def drop_money(self):
        Money(self.rect.x, self.rect.y, self.dropping_money)

    def intersect_with_knight(self):
        return pygame.sprite.collide_mask(self, main_character)


class Crawlid(Enemy):
    def __init__(self, x, y, graphics, *groups):
        super().__init__(x, y, graphics, *groups)

        self.hp = 2
        self.dropping_money = 3
        self.direction = -1
        self.count_reverse = 0

    def update(self):

        old_x = self.rect.x
        self.rect.x += self.direction * self.rect.width + self.direction * 10
        if not self.get_ver():
            self.direction *= -1
            self.cur_sheet = 1
            self.count_reverse = 1
            self.cur_frame = 0
        self.rect.x = old_x

        if self.cur_sheet == 1 and self.count_reverse == 3:
            self.count_reverse = 0
            self.count_flip = 0
            self.cur_sheet = self.cur_frame = 0

        if self.count_flip == 10:
            self.count_flip = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.cur_sheet])
            self.image = self.frames[self.cur_sheet][self.cur_frame]
            if self.direction == 1:
                self.image = pygame.transform.flip(self.image, True, False)

            self.mask = pygame.mask.from_surface(self.image)

            if self.count_reverse:
                self.count_reverse += 1

        if self.cur_sheet == 0:
            self.rect.x += self.direction

        self.count_flip += 1

        self.check_needs_of_damage()

    def check_needs_of_damage(self):
        if self.intersect_with_knight():
            main_character.get_damage(1)


class Money(pygame.sprite.Sprite):
    def __init__(self, x, y, amount):
        super().__init__(money)
        self.amount = amount
        image = load_image('money.png')
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        if pygame.sprite.spritecollideany(self, character):
            main_character.add_money(self.amount)
            self.kill()


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
        self.image = pygame.Surface((self.a, self.b))

        # начальное положение. Чтобы поменять self.rect.x = 100 или self.rect.y = 200
        self.rect = pygame.Rect(w // 2 + x, h // 2 + y, self.a, self.b)
        pygame.draw.rect(self.image, 'black', self.rect)


def initialization():
    global main_character, platforms, money, vertical_platforms, horizontal_platforms, enemies
    background = pygame.Surface(size)
    for group in [platforms, money, vertical_platforms, horizontal_platforms, enemies]:
        for sprite in group:
            sprite.kill()
            group.clear(screen, background)
            group.draw(screen)

    images = [(load_image('knight\knight_standing.png'), 1), (load_image('knight\knight_running.png'), 6),
              (load_image('knight\knight_falling.png'), 7),
              (load_image('knight\knight_in_jump.png', 'white'), 1),
              (load_image('knight\knight_sliding.png'), 4)
              ]
    graphics_knight = []
    for image, row in images:
        k = 130 / image.get_height()
        scaled_image = pygame.transform.scale(image, (
            image.get_width() * k, image.get_height() * k))
        graphics_knight.append((scaled_image, row, 1))
    # главный герой
    if main_character is None:
        main_character = Knight(0, 0, graphics_knight)
    else:
        main_character.health = 5
        main_character.healings = 6
        main_character.money = 0

    crawlids_graphics = []
    crawlids_images = [(load_image('crawlid\crawlid_walking.png'), 4), (load_image('crawlid\crawlid_reversing.png'), 2)]
    for image, row in crawlids_images:
        k = 80 / image.get_height()
        scaled_image = pygame.transform.scale(image, (
            image.get_width() * k, image.get_height() * k))
        crawlids_graphics.append((scaled_image, row, 1))

    enemies_cords = [(100, 16)]
    for x, y in enemies_cords:
        Crawlid(x, y, crawlids_graphics, enemies)

    cords = [(-100, -185, 69, 391), (-100, -185, 191, 68), (-100, 20, 102, 186), (-100, 20, 227, 34),
             (-100, 144, 647, 62),
             (-100, -185, 300, 31), (245, -185, 302, 68), (81, -185, 10, 180), (81, -68, 170, 17), (482, -185, 65, 391),
             (162, 40, 166, 66), (245, -185, 302, 31), (352, 38, 192, 74), (290, -72, 160, 17), (402, -17, 48, 30),
             (110, -115, 50, 20), (180, -130, 30, 10)]

    Money(1500, 1500, 25)

    for cord in cords:
        x, y, a, b = cord
        Platform(x + 1 / N, y, a - 2 / N, b, platforms, horizontal_platforms)
        Platform(x, y + 1 / N, a, b - 2 / N, platforms, vertical_platforms)


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
menu = pygame.sprite.Group()
money = pygame.sprite.Group()
N = 10
main_character = None
initialization()
