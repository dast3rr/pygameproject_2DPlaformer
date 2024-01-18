import sys

from graphics import platforms, screen, fps, size, \
    character, knight, enemies, main_character, menu, money, load_image, initialization, saving_points, \
    damage_waves, update_map_after_save, Money, money_list, new_game_confirmation, Crawlid, trigger_blocks, Sly, npcs, \
    sly_dialogue, sly_shop, background
from data import move_speed, start_jump_from_wall_position, start_jump_altitude, \
    fall_speed, global_cords, respawn_cords
import triggers
from menu import InGameMenu, Button, New_game_confirmation
import load_music
from music_volume_controller import volume_controller_filler, volume_controller_slider, volume_controller_base, \
    Base, Filler, Slider
from npc import Sly_dialogue, Sly_shop
from new_game_intro import new_game_intro

import pygame
import os

ATTACKING_SHEET = 5
SLIDING_SHEET = 4
JUMPING_SHEET = 3
FALLING_SHEET = 2
RUNNING_SHEET = 1
STANDING_SHEET = 0

SAVING_POINTS_CORDS = {'1': (-570, 7550), '2': (8780, 9220), '3': (9480, 7420), '4': (21500, 23500), '5': (24800, 22200)}

main_character_money = 0
volume = 0

lock_script = triggers.Boss_Wall_Lock()


def load_data_from_save():
    global respawn_cords, main_character_money, money_list, volume, main_character
    with open('../save/save.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        try:
            respawn_cords[0] = int(lines[0].split(':')[1].strip())
            respawn_cords[1] = int(lines[1].split(':')[1].strip())
            main_character_money = int(lines[2].split(':')[1].strip())
            for line in lines[3:-4]:
                collected = line.split(':')[1].split(', ')[4].strip()
                if collected == 'False':
                     money_list[lines.index(line) - 3][4] = False
                elif collected == 'True':
                    money_list[lines.index(line) - 3][4] = True
            volume = float(lines[-4].split(':')[1].strip())
            main_character.attack_damage = int(lines[-3].split(':')[1].strip())
            main_character.maximum_health = int(lines[-2].split(':')[1].strip())
            main_character.maximum_healings = int(lines[-1].split(':')[1].strip())
        except:
            print('Файл сохранения повреждён, начните новую игру.')
            write_data_to_save()


def write_data_to_save():
    global money_list, main_character, volume
    with open('../save/save.txt', 'w', encoding='utf-8') as f:
        f.write(f'respawn_x: {str(respawn_cords[0])}\n')
        f.write(f'respawn_y: {str(respawn_cords[1])}\n')
        f.write(f'main_character_money: {str(main_character_money)}\n')
        for coin in money_list:
            f.write(f'money: {", ".join([str(el) for el in coin])}\n')

        f.write(f'volume: {str(volume)}\n')
        f.write(f'main_character_attack_damage: {str(main_character.attack_damage)}\n')
        f.write(f'main_character_maximum_health: {str(main_character.maximum_health)}\n')
        f.write(f'main_character_maximum_healings: {str(main_character.maximum_healings)}\n')


# класс камеры
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.x = size[0] // 2
        self.y = size[1] // 2
        self.summary_d_x, self.summary_d_y = 0, 0

    # позиционировать камеру на объекте target
    def update(self):
        global start_jump_altitude, start_jump_from_wall_position, global_cords

        d_x = main_character.rect.x - self.x
        d_y = main_character.rect.y - self.y

        r = 15 * N
        k = 0

        if d_x > r:
            k = -1
        elif d_x < -r:
            k = 1
        if k:
            main_character.rect.x -= d_x + r * k
            self.x = main_character.rect.x + r * k
            self.summary_d_x += (d_x + r * k)

            start_jump_from_wall_position -= (d_x + r * k)
            for group in [platforms, money, enemies, saving_points, trigger_blocks, npcs]:
                for sprite in group:
                    if type(sprite) == Crawlid:
                        sprite.start_x -= (d_x + r * k)
                    sprite.rect.x -= (d_x + r * k)
        k = 0
        if d_y > r:
            k = -1
        elif d_y < -r:
            k = 1

        if k:
            main_character.rect.y -= d_y + r * k
            global_cords[1] -= d_y + r * k
            self.y = main_character.rect.y + r * k
            self.summary_d_y += (d_y + r * k)
            start_jump_altitude -= (d_y + r * k)
            for group in [platforms, money, enemies, saving_points, trigger_blocks, npcs]:
                for sprite in group:
                    sprite.rect.y -= (d_y + r * k)


def main_menu(screen):
    global respawn_cords, main_character_money, volume
    global start_jump_altitude, start_jump_from_wall_position, money_list
    global jump, jump_from_wall, speeds_before_jump, count_fall, counter_fall, game_paused, right, left

    load_music.main_menu_music()
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1, fade_ms=50)

    confirmation = New_game_confirmation()

    base = Base()
    slider = Slider()
    filler = Filler()

    background = pygame.transform.scale(load_image('main_menu_background_2.png'),
                                        (screen.get_width(), screen.get_height()))
    current_bg = 1
    change_bg_button = Button(400, 50, screen.get_width() // 2 - 200, screen.get_height() - 75,
                              (0, 0, 0, 0), (255, 255, 255, 100))

    new_game_button = Button(300, 100, screen.get_width() // 2 - 150, 300, (50, 50, 50), (255, 255, 255, 100))
    continue_button = Button(300, 100, screen.get_width() // 2 - 150, 450,
                             (50, 50, 50), (255, 255, 255, 20), (0, 0, 0, 100))
    exit_game_button = Button(300, 100, screen.get_width() // 2 - 150, 600, (50, 50, 50), (255, 255, 255, 100))

    start_new_game = False
    confirm_new_game = False

    how_to_play = False
    how_to_play_button = Button(200, 50, screen.get_width() - 250, 25,
                                (0, 0, 0, 100), (255, 255, 255, 100))
    how_to_play_font_color = pygame.Color('white')
    back_button = Button(300, 50, screen.get_width() // 2 - 150, screen.get_height() - 75,
                         (0, 0, 0, 100), (255, 255, 255, 100))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if change_bg_button.get_pressed() and not confirm_new_game and not how_to_play:
                    if current_bg == 1:
                        current_bg = 2
                        background = pygame.transform.scale(load_image('main_menu_background_1.jpg'),
                                                            (screen.get_width(), screen.get_height()))
                        how_to_play_font_color = (60, 60, 70)
                    elif current_bg == 2:
                        current_bg = 1
                        background = pygame.transform.scale(load_image('main_menu_background_2.png'),
                                                            (screen.get_width(), screen.get_height()))
                        how_to_play_font_color = pygame.Color('White')
                if how_to_play_button.get_pressed() and not confirm_new_game and not how_to_play:
                    how_to_play = True
                if back_button.get_pressed() and how_to_play:
                    how_to_play = False
                if new_game_button.get_pressed() and not confirm_new_game and not how_to_play:
                    if respawn_cords[0] and respawn_cords[1]:
                        confirm_new_game = True
                    else:
                        start_new_game = True
                if continue_button.get_pressed() and not confirm_new_game and not how_to_play:
                    data = upload_data()
                    start_jump_altitude, start_jump_from_wall_position, jump, jump_from_wall = data[:4]
                    speeds_before_jump, count_fall, counter_fall, game_paused, \
                        right, left, condition_damage_effects, dialogue_with_sly = data[4:]

                    load_music.first_loc_music()
                    pygame.mixer.music.play(-1, fade_ms=50)

                    slider.kill()
                    filler.kill()
                    return
                if exit_game_button.get_pressed() and not confirm_new_game and not how_to_play:
                    write_data_to_save()
                    pygame.quit()
                    sys.exit()
            slider.update(event)
            filler.update()

        screen.blit(background, (0, 0))


        if respawn_cords[0] and respawn_cords[1]:
            continue_button.disabled_color = None

        if how_to_play:
            back_button.draw('Назад', 30)
            font = pygame.font.Font(None, 35)
            texts = ['A, D - Передвижение', 'ПРОБЕЛ - Прыжок', 'Левая кнопка мыши - Атака', 'H - Лечение',
                     'E - Взаимодействие', 'Деньги остаются на месте смерти.',
                     'Враги возрождаются после смерти и после взаимодействия с точкой сохранения.',
                     'Хорошей игры!']
            for el in texts:
                text = font.render(el, 1, how_to_play_font_color)
                screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
                                   screen.get_height() // 4 + text.get_height() * 2 * texts.index(el)))

        if confirm_new_game:
            new_game_confirmation.draw(screen)
            confirmation.draw_buttons()
            new_game_confirmation.update()
        if confirmation.confirm_button.get_pressed() and confirm_new_game:
            start_new_game = True
            confirm_new_game = False
        if confirmation.reject_button.get_pressed() and confirm_new_game:
            confirm_new_game = False

        if start_new_game:
            respawn_cords[0] ,respawn_cords[1] = 0, 0
            main_character_money = 0
            main_character.attack_damage = 1
            main_character.maximum_health = 5
            main_character.maximum_healings = 6
            for coin in money_list:
                money_list[money_list.index(coin)][4] = False
            data = upload_data()

            start_jump_altitude, start_jump_from_wall_position, jump, jump_from_wall = data[:4]
            speeds_before_jump, count_fall, counter_fall, game_paused, \
            right, left, condition_damage_effects, dialogue_with_sly = data[4:]

            load_music.first_loc_music()
            pygame.mixer.music.play(-1, fade_ms=50)

            slider.kill()
            filler.kill()
            new_game_intro()
            return

        if not confirm_new_game and not how_to_play:
            new_game_button.draw('Новая игра', 40)
            continue_button.draw('Продолжить', 40)
            exit_game_button.draw('Выйти из игры', 40)
            how_to_play_button.draw('Как играть', 30)
            change_bg_button.draw('Сменить задний фон', 30)

            font = pygame.font.Font(None, 40)
            text = font.render('Громкость', True, pygame.Color('White'))
            screen.blit(text, (275, 50))

            volume_controller_base.draw(screen)
            pygame.draw.rect(screen, (255, 255, 255), filler.rect, border_radius=10)
            volume_controller_slider.draw(screen)
            volume = pygame.mixer.music.get_volume()

        pygame.display.flip()


def upload_data():
    global main_character, global_cords, money_list
    start_jump_altitude = -100000
    start_jump_from_wall_position = 0
    jump = False
    jump_from_wall = False
    speeds_before_jump = [0, 0]
    lock_script.lock_wall = False

    count_fall = False
    counter_fall = 0
    game_paused = False
    dialogue_with_sly = False
    # перемещение в стороны
    right = left = 0
    if respawn_cords[0] and respawn_cords[1]:
        main_character.rect.x = respawn_cords[0]
        main_character.rect.y = respawn_cords[1]
    condition_damage_effects = False

    camera.summary_d_x, camera.summary_d_y = 0, 0

    initialization(money_list, main_character_money)

    return (start_jump_altitude, start_jump_from_wall_position, jump, jump_from_wall, speeds_before_jump, count_fall,
            counter_fall, game_paused, right, left, condition_damage_effects, dialogue_with_sly)


def check_dead(camera):
    global start_jump_altitude, start_jump_from_wall_position, jump, jump_from_wall, money_list, global_y, global_x
    global speeds_before_jump, count_fall, counter_fall, game_paused, right, left, condition_damage_effects, dialogue_with_sly
    global respawn_cords, main_character_money, lock_script
    if not main_character.health:
        x, y = main_character.rect.x, main_character.rect.y
        lost_money_x, lost_money_y = x + camera.summary_d_x, y + camera.summary_d_y

        for sprite in damage_waves:
            sprite.kill()

        lost_money = main_character.money

        damage_waves.draw(screen)
        data = upload_data()

        start_jump_altitude, start_jump_from_wall_position, jump, jump_from_wall = data[:4]
        speeds_before_jump, count_fall, counter_fall, game_paused, right, left,\
        condition_damage_effects, dialogue_with_sly = data[4:]

        main_character.money = 0
        main_character_money = main_character.money
        main_character.healings = 2
        main_character.health = main_character.maximum_health

        main_character.update_heals()
        main_character.update_money()
        main_character.update_healthbar()


        lost_money_coin = Money(lost_money_x, lost_money_y, lost_money)
        write_data_to_save()


if __name__ == '__main__':
    # Перемещаю экран на центр
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    camera = Camera()
    stop_screen = screen.copy()

    data = upload_data()
    load_data_from_save()

    start_jump_altitude, start_jump_from_wall_position, jump, jump_from_wall = data[:4]
    speeds_before_jump, count_fall, counter_fall, game_paused, right, left, condition_damage_effects, dialogue_with_sly = data[4:]

    N = 10

    pygame.init()
    pygame.display.set_mode(size)
    # таймер для обновления фпс - 60
    clock = pygame.time.Clock()

    paused_menu = InGameMenu()
    dialogue_with_sly_window = Sly_dialogue()
    shop = Sly_shop()

    smooth_surface = pygame.Surface(size)
    smooth_surface.set_alpha(60)

    running = True

    main_menu(screen)

    background_image = load_image('background.png')
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    mouse_clicked_for_dialogues = False  # без этой переменной фразы в диалоге проматываются слишком быстро

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
                if keys[pygame.K_h]:
                    main_character.heal()

                if keys[pygame.K_ESCAPE]:
                    if not game_paused and not dialogue_with_sly:
                        game_paused = True
                    elif dialogue_with_sly:
                        dialogue_with_sly = False
                        dialogue_with_sly_window.open_shop = False
                    elif game_paused:
                        game_paused = False
                    write_data_to_save()


                if keys[pygame.K_e]:
                    for sprite in saving_points:
                        if sprite.can_save:
                            respawn_cords[0], respawn_cords[1] = SAVING_POINTS_CORDS[sprite.point_id]
                            update_map_after_save(camera)
                            write_data_to_save()
                    for sprite in npcs:
                        if sprite.can_talk:
                            dialogue_with_sly = True

                # при нажатии на пробел - прыжок
                if event.key == pygame.K_SPACE and (main_character.get_hor() or main_character.get_ver()):
                    start_jump_altitude = main_character.rect.y + 1
                    # проверка на зацепление за текстуры(был баг без этого)
                    main_character.rect.y -= 2
                    if main_character.get_ver() and main_character.get_hor():
                        main_character.rect.x += 1
                        if main_character.get_ver():
                            main_character.rect.x -= 2
                    # объявляю прыжок
                    jump = True
                    if main_character.get_ver():  # если есть касани вертикально стены, то объявляю прыжок от стены
                        jump_from_wall = True
                        speeds_before_jump = [0, 0]
                        main_character.rect.x -= 1
                        # запоминаю скорости
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not main_character.attack:
                    main_character.start_attacking()
                mouse_clicked_for_dialogues = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked_for_dialogues = False

        # цвет можно поменять. Это будет цвет фона
        # screen.fill(pygame.color.Color(200, 200, 200))
        screen.blit(background_image, (0, 0))

        # перемещение в стороны
        move_hor = right + left
        if main_character.get_hor() or main_character.get_ver():
            count_fall = False

        if not main_character.get_hor() and not jump and not count_fall:
            count_fall = True
            counter_fall = 0

        # определение скорости падения
        if main_character.get_ver() and not jump:

            fall_speed = 15 * N + counter_fall
            count_fall = False
            counter_fall = 0
            main_character.cur_sheet = SLIDING_SHEET

        elif not jump:
            fall_speed = 45 * N + counter_fall
        if jump:
            # при прыжке, на самой верхней точке скорость меньше
            fall_speed = -(25 * N - start_jump_altitude + main_character.rect.y) * 7
            if fall_speed > -20:
                counter_fall = 0
                count_fall = True
                jump = False
                fall_speed = 45 * N
        # если совершается прыжок от стены
        if jump_from_wall:
            # если уже далеко от стены
            if abs(main_character.rect.x - start_jump_from_wall_position) > 2 * N:
                jump_from_wall = False
                right, left = speeds_before_jump
                speeds_before_jump = [0, 0]

        camera.update()
        background.draw(screen)
        # отрисовываю все группы спрайтов
        platforms.draw(screen)
        platforms.update()
        money.draw(screen)
        money.update()
        character.draw(screen)
        enemies.update()
        enemies.draw(screen)

        npcs.update()
        npcs.draw(screen)

        saving_points.update()
        saving_points.draw(screen)

        trigger_blocks.update()
        trigger_blocks.draw(screen)

        if game_paused:
            screen.blit(smooth_surface, (0, 0))
            menu.draw(screen)
            InGameMenu.draw_menu_buttons(paused_menu)

            font = pygame.font.Font(None, 40)
            text = font.render(f'Урон от атаки: {main_character.attack_damage}', 1, pygame.Color('white'))
            screen.blit(text, (40, screen.get_height() - 200))

            text = font.render(f'Максимальное здоровье: {main_character.maximum_health}', 1, pygame.Color('white'))
            screen.blit(text, (40, screen.get_height() - 150))

            text = font.render(f'Максимум лечений: {main_character.maximum_healings}', 1, pygame.Color('white'))
            screen.blit(text, (40, screen.get_height() - 100))

            if paused_menu.resume_button.get_pressed():
                game_paused = False
            if paused_menu.back_to_main_menu_button.get_pressed():
                game_paused = False
                main_character_money = main_character.money
                write_data_to_save()
                main_menu(screen)

        if dialogue_with_sly:
            screen.blit(smooth_surface, (0, 0))

            if not dialogue_with_sly_window.open_shop:
                sly_dialogue.draw(screen)
                dialogue_with_sly_window.draw_buttons()

                if mouse_clicked_for_dialogues:
                    if dialogue_with_sly_window.close_dialogue_button.get_pressed():
                        dialogue_with_sly = False
                    if dialogue_with_sly_window.next_phrase_button and dialogue_with_sly_window.next_phrase_button.get_pressed():
                        dialogue_with_sly_window.current_phrase += 1
                    if dialogue_with_sly_window.shop_button and dialogue_with_sly_window.shop_button.get_pressed():
                        dialogue_with_sly_window.open_shop = True

                    mouse_clicked_for_dialogues = False
            else:
                sly_shop.draw(screen)
                shop.draw_buttons()

                font = pygame.font.Font(None, 35)
                text = font.render(f'Ваши деньги: {main_character.money}', 1, pygame.Color('white'))
                screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 40))
                if shop.close_button.get_pressed():
                    dialogue_with_sly_window.open_shop = False

                if mouse_clicked_for_dialogues:
                    if shop.buy_attack_improvement.get_pressed():
                        if main_character.money >= shop.damage_improvement_price:
                            main_character.money -= shop.damage_improvement_price
                            main_character.attack_damage += 1
                    if shop.buy_maximum_health_improvement.get_pressed():
                        if main_character.money >= shop.maximum_health_improvement_price:
                            main_character.money -= shop.maximum_health_improvement_price
                            main_character.maximum_health += 1
                    if shop.buy_maximum_healings_improvement.get_pressed():
                        if main_character.money >= shop.maximum_healings_improvement_price:
                            main_character.money -= shop.maximum_healings_improvement_price
                            main_character.maximum_healings += 1

                    mouse_clicked_for_dialogues = False

                sly_shop.update()

            sly_dialogue.update()

        elif not condition_damage_effects:
            jump = main_character.update(move_hor, jump, move_speed, fall_speed)
            enemies.update()
        else:
            main_character.update_damage_resistant()

        if count_fall:
            counter_fall += 6
            if counter_fall == 6:
                main_character.cur_sheet = FALLING_SHEET
                main_character.cur_frame = 0
        elif not move_hor and main_character.get_hor():
            main_character.cur_sheet = STANDING_SHEET
            counter_fall = 0
            count_fall = False
        else:
            main_character.cur_sheet = RUNNING_SHEET

        if jump:
            main_character.cur_sheet = JUMPING_SHEET

        if main_character.attack:
            main_character.cur_sheet = ATTACKING_SHEET

        if main_character.stop_screen and not condition_damage_effects:
            stop_screen = screen.copy()
            condition_damage_effects = True
        if not main_character.stop_screen:
            condition_damage_effects = False

        check_dead(camera)

        if main_character.stop_screen:
            counter_fall = 0
            screen.blit(stop_screen, (0, 0))

        pygame.display.flip()
        clock.tick(fps)
    write_data_to_save()
    pygame.quit()
