from graphics import Platform, platforms, screen, fps, size
from data import cords

import pygame
import os


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    for cord in cords:
        Platform(*cord)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.color.Color(200, 200, 200))
        platforms.draw(screen)
        platforms.update()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
