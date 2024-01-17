from graphics import main_character, Platform, platforms, vertical_platforms, horizontal_platforms
from data import global_cords, N, respawn_cords


boss_fight = False


def update_walls_for_boss():
    global boss_fight
    if global_cords[0] + respawn_cords[0] > 950 and global_cords[1] + respawn_cords[1] > 800 and not boss_fight:
        boss_fight = True
        x, y, a, b = 790, 680, 10, 700
        Platform(x + 1 / N, y, a - 2 / N, b, platforms, horizontal_platforms)
        Platform(x, y + 1 / N, a, b - 2 / N, platforms, vertical_platforms)
