import pygame
from graphics import menu, screen

class InGameMenu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(menu)
        self.image = pygame.Surface((screen.get_width() // 5, screen.get_height() // 3), pygame.SRCALPHA, 32)
        x, y = screen.get_width() // 2 - screen.get_width() // 10, screen.get_height() // 2 - screen.get_height() // 6
        pygame.draw.rect(self.image, pygame.Color('blue'), self.image.get_rect())
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

        self.resume_button = Button(self.image.get_width() // 2, self.image.get_height() // 6,
                                    self.rect.x + self.rect.width // 4, self.rect.y + self.rect.height // 5,
                                    pygame.Color('Black'), pygame.Color('Grey'), self.image)
        self.back_to_main_menu_button = Button(self.image.get_width() // 2, self.image.get_height() // 6,
                                               self.rect.x + self.rect.width // 4,
                                               self.rect.y + self.rect.height - self.rect.height // 5 -
                                               self.image.get_height() // 6,
                                               pygame.Color('Black'), pygame.Color('Grey'), self.image)

    def draw_menu_buttons(self):
        self.resume_button.draw()
        self.back_to_main_menu_button.draw()


class Button:
    def __init__(self, width, height, x, y, inactive_color, active_color, surface):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.x = x
        self.y = y

    def draw(self, message=None, action=None):
        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()

        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.width, self.height))

    def get_pressed(self):
        if self.x < pygame.mouse.get_pos()[0] < self.x + self.width and \
                self.y < pygame.mouse.get_pos()[1] < self.y + self.height and pygame.mouse.get_pressed()[0] == 1:
            return True
        return False