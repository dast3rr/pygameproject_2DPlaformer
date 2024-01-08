import pygame
from graphics import menu, screen

class InGameMenu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(menu)
        self.image = pygame.Surface((screen.get_width() // 8, screen.get_height() // 4), pygame.SRCALPHA, 32)
        x, y = screen.get_width() // 2 - screen.get_width() // 10, screen.get_height() // 2 - screen.get_height() // 6
        pygame.draw.rect(self.image, (0, 0, 0, 100), self.image.get_rect(), border_radius=50)
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

        self.resume_button = Button(self.rect.width // 2, self.rect.height // 8,
                                    self.rect.x + self.rect.width // 4, self.rect.y + self.rect.height // 4,
                                    (0, 0, 0, 0), (255, 255, 255, 20))
        self.back_to_main_menu_button = Button(self.rect.width // 2, self.rect.height // 8,
                                               self.rect.x + self.rect.width // 4,
                                               self.rect.y + self.rect.height - self.rect.height // 5 -
                                               self.rect.height // 8,
                                               (0, 0, 0, 0), (255, 255, 255, 20))

    def draw_menu_buttons(self):
        self.resume_button.draw('Вернуться в игру', 25)
        self.back_to_main_menu_button.draw('Главное меню', 25)


class Button:
    def __init__(self, width, height, x, y, inactive_color, active_color, disabled_color = None):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.disabled_color = disabled_color
        self.x = x
        self.y = y

    def draw(self, message=None, font_size=None):
        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()

        if not self.disabled_color:
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
                self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, self.active_color, self.image.get_rect(), border_radius=10)
                screen.blit(self.image, (self.x, self.y))
            else:
                self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, self.inactive_color, self.image.get_rect(), border_radius=10)
                screen.blit(self.image, (self.x, self.y))
        else:
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
            pygame.draw.rect(self.image, self.disabled_color, self.image.get_rect(), border_radius=10)
            screen.blit(self.image, (self.x, self.y))

        if message:
            font = pygame.font.Font(None, font_size)
            text = font.render(message, True, pygame.Color('White'))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                                         self.y + (self.height / 2 - text.get_height() / 2)))

    def get_pressed(self):
        if not self.disabled_color:
            if self.x < pygame.mouse.get_pos()[0] < self.x + self.width and \
                    self.y < pygame.mouse.get_pos()[1] < self.y + self.height and pygame.mouse.get_pressed()[0] == 1:
                return True
        return False