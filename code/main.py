from graphics import Platform, platforms, screen, fps, size
from data import cords

import pygame
import os


if __name__ == '__main__':
    #Перемещаю экран на центр
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.display.set_mode(size)
    # таймер для обновления фпс - 60
    clock = pygame.time.Clock()

    # Создаю чёрные прямоугольники стен по кординатам из data.py
    for cord in cords:
        Platform(*cord)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # цвет можно поменять. Это будет цвет фона
        screen.fill(pygame.color.Color(200, 200, 200))

        # отрисовываю все прямоугольники
        platforms.draw(screen)
        platforms.update()

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
