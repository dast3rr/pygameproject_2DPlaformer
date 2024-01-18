import pygame
from graphics import menu, screen, new_game_confirmation

class InGameMenu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(menu)
        self.image = pygame.Surface((screen.get_width() // 8, screen.get_height() // 4), pygame.SRCALPHA, 32)
        x, y = screen.get_width() // 2 - screen.get_width() // 10, screen.get_height() // 2 - screen.get_height() // 6
        pygame.draw.rect(self.image, (0, 0, 0, 100), self.image.get_rect(), border_radius=50)
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

        self.resume_button = Button(self.rect.width // 2, self.rect.height // 8,
                                    self.rect.x + self.rect.width // 4, self.rect.y + self.rect.height // 4,
                                    (50, 50, 50), (255, 255, 255, 100))
        self.back_to_main_menu_button = Button(self.rect.width // 2, self.rect.height // 8,
                                               self.rect.x + self.rect.width // 4,
                                               self.rect.y + self.rect.height - self.rect.height // 5 -
                                               self.rect.height // 8,
                                               (50, 50, 50), (255, 255, 255, 100))

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
        self.c = 0


    def draw(self, message=None, font_size=None):
        mouse = pygame.mouse.get_pos()

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
                    self.y < pygame.mouse.get_pos()[1] < self.y + self.height and pygame.mouse.get_pressed()[0]:
                return True
        return False


class New_game_confirmation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(new_game_confirmation)
        self.image = pygame.Surface((screen.get_width() // 8, screen.get_height() // 6), pygame.SRCALPHA, 32)
        x, y = screen.get_width() // 2 - self.image.get_width() // 2, \
               screen.get_height() // 2 - self.image.get_height() // 2
        pygame.draw.rect(self.image, (0, 0, 0, 75), self.image.get_rect(), border_radius=50)
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

        self.confirm_button = Button(self.rect.width // 3, self.rect.height // 6,
                                self.rect.x + self.rect.width // 8,
                                self.rect.y + self.rect.height // 3 * 2,
                                (50, 50, 50), (255, 255, 255, 100))
        self.reject_button = Button(self.rect.width // 3, self.rect.height // 6,
                                self.rect.x + self.rect.width // 2 + self.rect.width // 16,
                                self.rect.y + self.rect.height // 3 * 2,
                                (50, 50, 50), (255, 255, 255, 100))

    def update(self):
        font = pygame.font.Font(None, 25)
        text = font.render('При начале новой игры', 1, pygame.Color('White'))
        screen.blit(text, (self.rect.x + (self.rect.width / 2 - text.get_width() / 2), self.rect.y + self.rect.w // 8))

        font = pygame.font.Font(None, 25)
        text = font.render('текущее сохранение сотрётся.', 1, pygame.Color('White'))
        screen.blit(text, (self.rect.x + (self.rect.width / 2 - text.get_width() / 2),
                           self.rect.y + self.rect.w // 8 + text.get_height() * 1.5))

        font = pygame.font.Font(None, 25)
        text = font.render('Начать новую игру?', 1, pygame.Color('White'))
        screen.blit(text, (self.rect.x + (self.rect.width / 2 - text.get_width() / 2),
                           self.rect.y + self.rect.w // 2 - text.get_height() * 2))

    def draw_buttons(self):
        self.confirm_button.draw('Да', 25)
        self.reject_button.draw('Нет', 25)