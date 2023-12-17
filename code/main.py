from graphics import Platform, platforms, screen, fps
import pygame
from screeninfo import get_monitors
import os

if __name__ == '__main__':
    monitor = get_monitors()[0]
    size = monitor.width, monitor.height
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('grey')
        platforms.draw(screen)
        platforms.update()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
